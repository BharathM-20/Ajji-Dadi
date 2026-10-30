"""Draft language guidance and few-shot examples; not weight training or native approval."""

# Author-written style examples, intentionally separate from held-out evaluation callers.
# They are prompt demonstrations only. No native-speaker review or training has occurred.
EXAMPLES = {
    "Hinglish": {
        "facts": (
            "Ghar mein Rohan aapke kya lagte hain?",
            "Rohan mera pota hai, main Savitri Devi bol rahi hoon.",
        )
    },
    "Hindi": {"facts": ("घर में रोहन आपके क्या लगते हैं?", "रोहन मेरा पोता है, मैं सावित्री देवी बोल रही हूँ।")},
    "Kannada": {
        "facts": ("ಮನೆಯಲ್ಲಿ ಪ್ರಶಾಂತ್ ನಿಮಗೆ ಏನಾಗಬೇಕು?", "ಪ್ರಶಾಂತ್ ನನ್ನ ಮೊಮ್ಮಗ, ನಾನು ಶಾರದಮ್ಮ ಮಾತನಾಡುತ್ತಿದ್ದೇನೆ.")
    },
}


INTENTS = {
    "facts": (
        r"\b(?:rohan|pota|pote|grandson|savitri|sharadamma|prashanth)\b|"
        r"(?:aapka|aapke|tumhara|your)\s+(?:naam|name)|karne wali.*naam|"
        r"रोहन|पोता|पोते|सावित्री|आपका नाम|आप किस नाम|"
        r"ಪ್ರಶಾಂತ್|ಮೊಮ್ಮಗ|ಶಾರದಮ್ಮ|(?:ನಿಮ್ಮ|ಮಾತನಾಡುತ್ತಿರುವವರ).{0,8}ಹೆಸರ"
    ),
    "recall": (
        r"pehle.*(?:kaunsa|kya)|kaunsa.*(?:vibhag|case)|earlier|"
        r"maine.*shuru.*kis.*(?:daftar|naam)|पहले.*(?:कौन|किस)|शुरू में.*किस.*(?:कार्यालय|दफ्तर)|"
        r"ಮೊದಲು.*(?:ಏನು|ಕಚೇರಿ)"
    ),
    "reading": r"message|sms|read|padh|screen|button|chashma|expired|संदेश|पढ़|पंक्ति|ಕೋಡ್|ಸಂದೇಶ|ಓದಿ|ಬಟನ್",
    "install": r"\b(?:install\w*|download\w*|permission|app)\b|ऐप|अनुमति|ಅನುಮತಿ|ಆಪ್|ಆ್ಯಪ್|ಡೌನ್",
    "otp": r"\botp\b|\bcode\b|ओटीपी|कोड|ಒಟಿಪಿ|ಕೋಡ್",
    "payment": r"\bupi\b|pay|transfer|money|paise|पैस|भुगतान|ಹಣ|ಪಾವತಿ|ಕಳಿಸಿ",
    "threat": r"arrest|police|giraftar|cbi|जेल|गिरफ्तार|पुलिस|ಪೊಲೀ|ಬಂಧ",
}

GOALS = {
    "facts": "Answer the requested persona facts and relationships directly; no unrelated stall.",
    "recall": "Answer using the caller's earlier claims, not your own bank. Do not invent a claim.",
    "reading": "Stay on the current message/screen. Do not fetch an item already found or put on.",
    "otp": "Delay locating/reading the message. Never request, repeat or disclose a secret code.",
    "payment": "Slow the payment request without paying or giving payment instructions.",
    "install": "Stay confused about the old phone's controls; never give installation steps.",
    "threat": "React mildly to the threat and ask one relevant clarification, without obeying it.",
    "general": "Answer the latest statement first, then make one believable small delay.",
}

TACTIC_ORDER = {
    "reading": ["glasses", "spell", "phone", "hearing", "pages", "notebook"],
    "otp": ["phone", "glasses", "hearing", "spell", "notebook"],
    "payment": ["bankbook", "notebook", "pen", "pages", "calendar"],
    "install": ["glasses", "phone", "spell", "hearing", "grandson"],
    "threat": ["notebook", "hearing", "spell", "phone", "glasses"],
}
