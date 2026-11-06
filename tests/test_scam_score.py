"""Rule-based score checks use synthetic text only and make no model/provider calls."""

from src import scam_score


def log(*caller_text):
    return [{"who": "caller", "text": text} for text in caller_text]


def test_sensitive_request_plus_authority_and_threat_scores_high():
    result = scam_score.analyze(
        log(
            "I am calling from the bank security team.",
            "Tell me your OTP now or your account will be blocked.",
        )
    )
    assert result["score"] == 10
    assert result["label"] == "Likely scam"
    assert result["recommendation"] is True
    assert "credential request" in result["signals"]
    assert "authority claim" in result["signals"]


def test_delivery_code_is_not_scored_as_a_bank_credential_scam():
    result = scam_score.analyze(log("Swiggy delivery at the gate, please tell me the OTP."))
    assert result["score"] == 1
    assert result["recommendation"] is False


def test_payment_mention_without_a_demand_does_not_add_payment_points():
    result = scam_score.analyze(log("I am calling about your bank payment receipt."))
    assert result["score"] == 0
    assert "payment demand" not in result["signals"]


def test_explicit_payment_demand_counts_as_a_risk_signal():
    result = scam_score.analyze(log("Transfer money to this account now."))
    assert result["score"] == 3
    assert "payment demand" in result["signals"]


def test_only_caller_lines_count_not_dadis_repeated_code_questions():
    result = scam_score.analyze(
        [
            {"who": "bot", "text": "Tell me your OTP?"},
            {"who": "caller", "text": "I called about your appointment."},
        ]
    )
    assert result["score"] == 0
    assert result["signals"] == []


def test_telugu_script_patterns_are_detected():
    result = scam_score.analyze(
        log("నేను బ్యాంకు అధికారి.", "మీ ఖాతా బ్లాక్ అవుతుంది, ఓటీపీ చెప్పండి.")
    )
    assert result["score"] >= 7
    assert result["recommendation"] is True


def test_kannada_script_patterns_are_detected():
    result = scam_score.analyze(
        log("ನಾನು ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ.", "ಖಾತೆ ಮುಚ್ಚುತ್ತದೆ, ಒ ಟಿ ಪಿ ಹೇಳಿ.")
    )
    assert result["score"] >= 7


def test_no_caller_speech_has_no_fabricated_score():
    result = scam_score.analyze([{"who": "bot", "text": "OTP"}])
    assert result == {
        "score": None,
        "label": "Insufficient caller speech",
        "signals": [],
        "recommendation": False,
    }
