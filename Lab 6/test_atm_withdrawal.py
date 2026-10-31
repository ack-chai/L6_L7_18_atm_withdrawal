import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------------------------------------------------------
# Branch Coverage Tests for withdraw()
# ---------------------------------------------------------
def test_withdraw_unknown_account():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(10000, 1000, "credit", True)


def test_withdraw_amount_less_than_or_equal_zero():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 0, "savings", True)


def test_withdraw_amount_not_multiple_of_100():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 150, "savings", True)


def test_withdraw_limit_exceeded():
    assert withdraw(50000, 30000, "savings", True) == "limit exceeded"


def test_withdraw_own_bank_success():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_withdraw_other_bank_low_amount():
    assert withdraw(10000, 5000, "savings", False) == 4980


def test_withdraw_other_bank_high_amount():
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_withdraw_current_account_success():
    assert withdraw(60000, 40000, "current", True) == 20000


def test_withdraw_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


# ---------------------------------------------------------
# Branch Coverage Tests for pin_check()
# ---------------------------------------------------------
def test_pin_check_attempts_greater_than_or_equal_3():
    assert pin_check(1234, 1234, 3) == "card blocked"
    assert pin_check(1234, 1234, 4) == "card blocked"


def test_pin_check_entered_equals_actual():
    assert pin_check(1234, 1234, 0) == "ok"
    assert pin_check(1234, 1234, 2) == "ok"


def test_pin_check_last_attempt_failed():
    assert pin_check(9999, 1234, 2) == "card blocked"


def test_pin_check_retry():
    assert pin_check(9999, 1234, 0) == "retry"
    assert pin_check(9999, 1234, 1) == "retry"


# ---------------------------------------------------------
# Branch Coverage Tests for note_breakup()
# ---------------------------------------------------------
def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(250)


def test_note_breakup_remaining_greater_equal_200():
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_remaining_less_than_200():
    assert note_breakup(600) == (1, 0, 1)
    assert note_breakup(500) == (1, 0, 0)
