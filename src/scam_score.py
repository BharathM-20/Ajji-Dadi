"""Small, explainable scam-risk heuristic applied only to caller statements."""

import re

_CODE = re.compile(
    r"\botp\b|one.?time.?password|verification code|pin|password|"
    r"ओ\s*टी\s*पी|ओटीपी|पिन|पासवर्ड|"
    r"ಒ\s*ಟಿ\s*ಪಿ|ಓ\s*ಟಿ\s*ಪಿ|ಒ\s*ಟಿಪಿ|ಓ\s*ಟಿಪಿ|ಪಿನ್|ಪಾಸ್ವರ್ಡ್|"
    r"ఓటీపీ|ఓటిపి|ఒటిపి|పిన్|పాస్.?వర్డ్",
    re.I,
)
_ASK = re.compile(
    r"\b(tell|share|send|give|read|say|provide|confirm|batao|bataiye|boliye|bhejo|heli|helu|kodi)\b|"
    r"बताइए|बताओ|दीजिए|बोलिए|शेयर|भेजिए|"
    r"ಹೇಳಿ|ಹೇಳು|ಕೊಡಿ|ಕಳುಹಿಸಿ|ನಮೂದಿಸಿ|"
    r"చెప్పండి|చెప్పు|ఇవ్వండి|పంపండి|చదవండి",
    re.I,
)
_PAYMENT = re.compile(
    r"\b(?:send|transfer|pay|deposit|wire)\b.{0,40}\b(?:money|payment|fee|"
    r"rupees?|lakh|upi)\b|\b(?:money|payment|fee|rupees?|lakh|upi)\b"
    r".{0,40}\b(?:send|transfer|pay|deposit|wire)\b|"
    r"पैसे? भेज|रुपये? भेज|रकम जमा|भुगतान करो|भुगतान करें|पैसा दो|"
    r"ಹಣ ಕಳುಹಿಸ|ಹಣ ಹಾಕಿ|ಪಾವತಿ ಮಾಡಿ|ಹಣ ವರ್ಗಾಯಿಸಿ|"
    r"డబ్బు పంప|డబ్బు వేయ|చెల్లించండి|బదిలీ చేయండి",
    re.I,
)
_REMOTE = re.compile(
    r"\b(anydesk|teamviewer|remote access|screen.?share|install this app|download this app)\b|"
    r"ಆ್ಯಪ್ ಇನ್.?ಸ್ಟಾಲ್|ಆಪ್ ಡೌನ್.?ಲೋಡ್|ಸ್ಕ್ರೀನ್.?ಶೇರ್|"
    r"యాప్ ఇన్.?స్టాల్|యాప్ డౌన్.?లోడ్|స్క్రీన్.?షేర్",
    re.I,
)
_AUTHORITY = re.compile(
    r"\b(cbi|police|trai|rbi|customs|cyber crime|bank officer|fraud team|"
    r"security team|income tax|court officer)\b|"
    r"सीबीआई|पुलिस|आरबीआई|बैंक अधिकारी|फ्रॉड टीम|"
    r"ಸಿಬಿಐ|ಪೊಲೀಸ್|ಆರ್ಬಿಐ|ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ|"
    r"సీబీఐ|పోలీసు|ఆర్బీఐ|బ్యాంకు అధికారి",
    re.I,
)
_THREAT = re.compile(
    r"\b(arrest|warrant|jail|account.{0,35}(?:block(?:ed)?|freeze(?:d)?|clos(?:e|ed|es))|"
    r"card.{0,35}block(?:ed)?|"
    r"case against you|urgent|immediately|right now|today only|deadline)\b|"
    r"गिरफ्तार|वारंट|जेल|खाता.{0,12}(?:बंद|ब्लॉक)|कार्ड.{0,12}ब्लॉक|अभी तुरंत|"
    r"ಬಂಧನ|ವಾರಂಟ್|ಜೈಲು|ಖಾತೆ.{0,12}(?:ಮುಚ್ಚು|ಬ್ಲಾಕ್)|ಕಾರ್ಡ್.{0,12}ಬ್ಲಾಕ್|ಇಗಲೇ|"
    r"అరెస్ట్|వారెంట్|జైలు|ఖాతా.{0,12}(?:మూసి|బ్లాక్)|కార్డు.{0,12}బ్లాక్|వెంటనే",
    re.I,
)
_SECRECY = re.compile(
    r"\b(don't tell|do not tell|keep.{0,12}secret|tell no one|stay on the line)\b|"
    r"किसी को मत बत|किसीसे मत कह|गुप्त रख|"
    r"ಯಾರಿಗೂ ಹೇಳಬೇಡ|ಯಾರಿಗೂ ಹೇಳಬೇಡಿ|ರಹಸ್ಯವಾಗಿರಲಿ|"
    r"ఎవరికీ చెప్పొద్దు|ఎవరికీ చెప్పకండి|రహస్యంగా ఉంచండి",
    re.I,
)
_DELIVERY = re.compile(
    r"\b(delivery|courier|swiggy|zomato|food order|parcel at the gate)\b|"
    r"ಡೆಲಿವರಿ|ಕೂರಿಯರ್|ಆರ್ಡರ್|ವಿತರಣೆ|డెలివరీ|కూరియర్|ఆర్డర్|పార్సెల్",
    re.I,
)


def caller_statements(log):
    """Return caller-only content; Dadi's own words never affect the score."""
    return [
        str(item.get("text", ""))[:600]
        for item in log
        if isinstance(item, dict) and item.get("who") in {"caller", "user"}
        and isinstance(item.get("text"), str) and item["text"].strip()
    ]


def analyze(log):
    """Score call-level risk from distinct evidence categories, capped at 10.

    Weights: credential request 3, payment demand 3, remote access 3, authority claim 2,
    threat/urgency 2, secrecy 2. Authority plus a dangerous demand adds 2; authority plus
    threat and another dangerous demand adds 1. Delivery OTPs without other risk signals score1.
    Thresholds: 0–3 lower signal, 4–6 review, 7–10 likely scam. These are prototype rules,
    not calibrated probabilities or a validated fraud classifier.
    """
    statements = caller_statements(log)
    text = " ".join(statements)
    if not text:
        return {
            "score": None,
            "label": "Insufficient caller speech",
            "signals": [],
            "recommendation": False,
        }

    code_request = bool(_CODE.search(text) and _ASK.search(text))
    payment = bool(_PAYMENT.search(text))
    remote = bool(_REMOTE.search(text))
    authority = bool(_AUTHORITY.search(text))
    threat = bool(_THREAT.search(text))
    secrecy = bool(_SECRECY.search(text))

    # A delivery OTP belongs to the order, not the recipient's bank account.
    if code_request and _DELIVERY.search(text) and not (payment or remote or threat or secrecy):
        return {
            "score": 1,
            "label": "Low signal",
            "signals": ["Delivery-related order code; no other listed pressure signal"],
            "recommendation": False,
        }

    points = {
        "credential request": (code_request, 3),
        "payment demand": (payment, 3),
        "remote-access instruction": (remote, 3),
        "authority claim": (authority, 2),
        "threat or urgency": (threat, 2),
        "secrecy pressure": (secrecy, 2),
    }
    signals = [label for label, (present, _) in points.items() if present]
    score = sum(weight for present, weight in points.values() if present)
    dangerous_demand = code_request or payment or remote
    if authority and dangerous_demand:
        score += 2
        signals.append("authority claim paired with a sensitive request")
    if authority and threat and (dangerous_demand or secrecy):
        score += 1
        signals.append("authority claim combined with pressure")
    score = min(10, score)
    label = "Likely scam" if score >= 7 else "Review carefully" if score >= 4 else "Low signal"
    return {
        "score": score,
        "label": label,
        "signals": signals,
        "recommendation": score >= 7,
    }
