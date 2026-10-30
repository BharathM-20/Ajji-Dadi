"""Reference classifier prompts, few-shot loader and keyword cross-checks."""

import json
import os
import re

from . import adapters
from .report import parse_json

CLASSIFY = (
    "You screen UNKNOWN phone calls in India (Hinglish / Kanglish, Latin script) for "
    "the phone's owner.\n"
    "Given the screening transcript (CALLER = unknown caller), return ONLY JSON:\n"
    '{"reason_for_call": str, "scam_score": 0-10, "signals": [exact caller phrases], '
    '"verdict": "legit"|"suspicious"|"scam"}\n'
    "\n"
    'Most unknown calls are ordinary. Default to "legit" unless the caller\'s own '
    "words show a scam pattern.\n"
    "\n"
    "SAME WORDS, DIFFERENT CONTEXT (this is where mistakes happen):\n"
    "- OTP: a delivery agent, cab driver or gas-cylinder boy asking for the OTP of "
    "an order/ride the owner placed\n"
    '  is NORMAL. An OTP request is a scam signal only when paired with "your '
    'account/card is at risk",\n'
    "  a fake bank/fraud team, a remote-access app, threats, secrecy, or money demands.\n"
    '- Parcel: a courier at the gate asking for address/OTP is normal. "Your parcel '
    'was caught at customs / has drugs"\n'
    "  plus a fine or video call is a scam.\n"
    '- Bank: a branch saying "come collect your cheque book, no OTP needed" is '
    'normal. "KYC pending, click link",\n'
    '  "card will be blocked, share OTP" is phishing.\n'
    "- Authority: clinic/school/society/recruiter calls with no demand are normal. "
    "CBI/police/TRAI/customs/RBI\n"
    "  calling about a case against the owner is a scam: real agencies do not arrest "
    "or take payment over a phone call.\n"
    "- Friend on a new number is fine until money is asked for. Wrong numbers are harmless.\n"
    "\n"
    'SCAM SIGNALS: fake authority; arrest/warrant/case threat; deadline ("2 ghante '
    'me", "aaj raat"); payment by UPI/transfer to a\n'
    'personal number; "tell no one"/"kisi ko mat batana"; "stay on video"; '
    "AnyDesk/TeamViewer/download an app;\n"
    "advance or processing fee; guaranteed returns; emotional emergency + money.\n"
    "STRONG SCAM = fake authority + urgency/threat + (money or secrecy or remote app).\n"
    "SUSPICIOUS = spam or phishing shape without a hard threat or payment demand yet "
    "(loan/insurance sales, prize bait,\n"
    '"click link to update KYC/address"). Thin or mixed evidence = "suspicious", '
    'never "scam".\n'
    "\n"
    "Every signal must quote words the caller actually said. Do not invent signals. "
    "Use only the transcript."
)

CLAIM_PATTERNS = {
    "authority": (
        r"\b(cbi|police|trai|rbi|customs|narcotics|cyber ?crime|bank officer|"
        r"fraud team|fraud department|security team)\b"
    ),
    "pretext": r"\b(parcel|fedex|courier|aadhaar|sim|kyc|arrest|warrant|laundering|drugs)\b",
    "demand": r"\b(otp|upi|transfer|rupees?|lakh|video call|video)\b",
}


PRESSURE = (
    r"\b(transfer|upi|rupees?|lakh|arrest|warrant|video call|tell no one|kisi ko mat|mat batana|"
    r"abhi ke abhi|anydesk|teamviewer|processing fee|guaranteed|double|kat jayega|sim band|"
    r"card block|case hoga|yarigu helbedi|arrest aag)\b"
)


SCENARIO_PATHS = ["scenarios.json", "tests/fixtures/scenarios.json"]


FEWSHOT_IDS = [
    "L01_swiggy_otp",
    "L05_bank_branch",
    "L04_clinic",
    "B02_kyc_vague",
    "S08_fake_fraud_team",
    "S04_fake_fedex",
    "S01_digital_arrest",
    "L07_friend_new_number",
]


SCREENER_Q = {
    "hinglish": "Kaun bol raha hai, kis kaam ke liye call kiya?",
    "kanglish": "Yaaru matadtha idira, yaake call maadidri?",
}


def load_scenarios():
    for p in SCENARIO_PATHS:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as handle:
                return json.load(handle)["scenarios"]
    return []


def to_transcript(turns, lang="hinglish"):
    """Same shape the live screener produces: CALLER, SCREENER question, CALLER, SCREENER close."""
    q = SCREENER_Q.get(lang, SCREENER_Q["hinglish"])
    return f"CALLER: {turns[0]}\nSCREENER: {q}\nCALLER: {turns[1]}\nSCREENER: (closing line)"


def fewshot_messages():
    by_id = {s["id"]: s for s in load_scenarios()}
    out = []
    for sid in FEWSHOT_IDS:
        s = by_id.get(sid)
        if s:
            out += [
                {"role": "user", "content": to_transcript(s["caller_turns"], s["lang"])},
                {"role": "assistant", "content": json.dumps(s["expected"], ensure_ascii=False)},
            ]
    return out


def classify(transcript):
    r = parse_json(
        adapters.think(
            [
                {"role": "system", "content": CLASSIFY},
                *fewshot_messages(),
                {"role": "user", "content": transcript},
            ],
            True,
            300,
        )
    )
    r.setdefault("verdict", "suspicious")  # fail safe: borderline, human decides
    # plain-code second opinion on what the CALLER said (guards against overconfident LLM verdicts)
    caller = " ".join(
        line[7:] for line in transcript.splitlines() if line.startswith("CALLER:")
    ).lower()
    auth = bool(re.search(CLAIM_PATTERNS["authority"], caller))
    pressure = bool(re.search(PRESSURE, caller))
    if r["verdict"] == "scam" and not (auth or pressure):
        r["verdict"] = "suspicious"
        r["note"] = "downgraded: LLM said scam but no rule signals"
    elif r["verdict"] == "legit" and auth and pressure:
        r["verdict"] = "suspicious"
        r["note"] = "upgraded: authority claim + pressure words"
    return r
