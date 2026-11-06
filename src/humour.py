"""Small, adapted style references; no corpus loading, provider calls or canned replies."""

import re

# Adapted from supplied domain groups, not copied dialogue or verified native-language prose.
# Each match needs BOTH a concrete subject and its particular claim in the latest turn.
REFERENCES = (
    {
        "topic": "refund_fee", "source": "DADI-EN-0041 / DADI-KN-0041",
        "cues": (r"refund|receive money|रिफंड|पैसे वापस|ಮರುಪಾವತಿ|ರಿಫಂಡ್",
                 r"fee|pay|charge|शुल्क|फीस|भेज|ಪಾವತಿ|ಶುಲ್ಕ|ಕಳಿಸು"),
        "English": ("Pay a fee to receive your refund.",
                    "This refund has arrived with a shopping list of its own, beta."),
        "Hindi": ("रिफंड लेने के लिए पहले फीस भेजिए।",
                  "बेटा, ये रिफंड तो अपने साथ खर्चे की पूरी सूची लेकर आया है।"),
        "Kannada": ("ರಿಫಂಡ್ ಪಡೆಯಲು ಮೊದಲು ಶುಲ್ಕ ಕಳಿಸು.",
                    "ಮಗು, ಈ ರಿಫಂಡ್ ತನಗೇ ಖರ್ಚಿನ ಪಟ್ಟಿಯನ್ನು ಮಾಡಿಕೊಂಡು ಬಂದಿದೆಯಲ್ಲ."),
    },
    {
        "topic": "rental_deposit", "source": "DADI-EN-0641 / DADI-KN-0641",
        "cues": (r"\b(?:flat|rental|rent|house)\b|फ्लैट|किराय|मकान|ಬಾಡಿಗೆ|ಮನೆ|ಫ್ಲಾಟ್",
                 r"deposit|token|advance|जमा|टोकन|अग्रिम|एडवांस|ಮುಂಗಡ|ಟೋಕನ್|ಅಡ್ವಾನ್ಸ್"),
        "English": ("Send the deposit before viewing the flat.",
                    "If I imagine living there first, will you charge rent for that too?"),
        "Hindi": ("फ्लैट देखने से पहले एडवांस भेजिए।",
                  "बेटा, पहले वहाँ रहने का सपना देख लूँ तो उसका भी किराया लगेगा क्या?"),
        "Kannada": ("ಮನೆ ನೋಡುವ ಮೊದಲು ಮುಂಗಡ ಕಳಿಸು.",
                    "ಮಗು, ಮೊದಲು ಆ ಮನೆಯಲ್ಲಿ ಇರುವ ಕನಸು ಕಂಡರೆ ಅದಕ್ಕೂ ಬಾಡಿಗೆ ಕೊಡಬೇಕಾ?"),
    },
    {
        "topic": "guaranteed_returns", "source": "DADI-EN-0321 / DADI-KN-0321",
        "cues": (r"\b(?:investment|invest|money)\b|निवेश|पैस|रकम|ಹೂಡಿಕೆ|ಹಣ|ಲಾಭ",
                 r"double|guarantee|दोगुन|गारंटी|दुगुन|ಡಬಲ್|ದುಪ್ಪಟ್ಟು|ಗ್ಯಾರಂಟಿ"),
        "English": ("Your investment will double, guaranteed.",
                    "My money has become so hardworking; perhaps it can do my paperwork too."),
        "Hindi": ("आपके पैसे दोगुने होंगे, गारंटी है।",
                  "बेटा, मेरे पैसे इतने मेहनती हो गए, उनसे मेरा कागज़ी काम भी करवा दो।"),
        "Kannada": ("ನಿನ್ನ ಹಣ ದುಪ್ಪಟ್ಟಾಗುತ್ತದೆ, ಗ್ಯಾರಂಟಿ.",
                    "ಮಗು, ನನ್ನ ಹಣ ಇಷ್ಟು ಕೆಲಸ ಮಾಡುತ್ತದಂತೆ, ನನ್ನ ಕಾಗದದ ಕೆಲಸವನ್ನೂ ಅದಕ್ಕೇ ಕೊಟ್ಟರೆ ಹೇಗೆ?"),
    },
    {
        "topic": "account_deadline", "source": "DADI-EN-0001 / DADI-KN-0001",
        "cues": (r"account|खात|अकाउंट|ಖಾತೆ|ಅಕೌಂಟ್",
                 r"block|freez|close|बंद|ब्लॉक|फ्रीज|ಮುಚ್ಚ|ಬ್ಲಾಕ್|ಫ್ರೀಜ್"),
        "English": ("Your account will close today.",
                    "My account has decided to retire before me, has it?"),
        "Hindi": ("आपका खाता आज बंद हो जाएगा।",
                  "बेटा, खाते ने मुझसे पहले रिटायर होने की ठान ली क्या?"),
        "Kannada": ("ನಿನ್ನ ಖಾತೆ ಇವತ್ತು ಮುಚ್ಚುತ್ತದೆ.",
                    "ನನ್ನ ಖಾತೆ ನನಗಿಂತ ಮುಂಚೆಯೇ ನಿವೃತ್ತಿ ತಗೊಳ್ಳುತ್ತದೆಯಾ ಮಗು?"),
    },
)


def style_reference(text, language, history):
    """One optional reference for an unambiguous, new topic; history is never discarded."""
    native = {"Hinglish": "Hindi", "Kanglish": "Kannada"}.get(language, language)
    matches = [entry for entry in REFERENCES if all(
        re.search(cue, str(text), re.I) for cue in entry["cues"]
    )]
    if len(matches) != 1 or native not in matches[0]:
        return None
    entry = matches[0]
    # The same illustration is never supplied again once its topic occurs in Dadi history.
    if any(item["role"] == "user" and all(
        re.search(cue, str(item["content"]), re.I) for cue in entry["cues"]
    ) for item in history):
        return None
    caller, dadi = entry[native]
    return {"topic": entry["topic"], "example_caller": caller, "example_dadi": dadi}
