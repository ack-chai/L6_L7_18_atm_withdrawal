import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# 1. Tests for withdraw()
def test_withdraw_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(10000, 1000, "credit", True)


def test_withdraw_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, -100, "savings", True)


def test_withdraw_limit_exceeded():
    assert withdraw(50000, 30000, "savings", True) == "limit exceeded"


def test_withdraw_other_bank_high_amount():
    # Tests non-own bank with amount > 10000 (fee = 20 + 10 = 30)
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_withdraw_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_withdraw_success_own_bank():
    assert withdraw(5000, 1000, "savings", True) == 4000


# 2. Tests for pin_check()
def test_pin_check_attempts_exceeded():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_pin_check_success():
    assert pin_check(1234, 1234, 0) == "ok"


def test_pin_check_last_attempt_failed():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_pin_check_retry():
    assert pin_check(1111, 1234, 1) == "retry"


# 3. Tests for note_breakup()
def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_with_200_notes():
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_without_200_notes():
    assert note_breakup(500) == (1, 0, 0)
