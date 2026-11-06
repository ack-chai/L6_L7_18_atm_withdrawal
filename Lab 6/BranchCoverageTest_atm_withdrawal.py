import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------------------------------------------------------
# Branch Coverage Tests for withdraw()
# ---------------------------------------------------------
def test_withdraw_unknown_account():
    # Branch: account_type not in DAILY_LIMIT -> True
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(10000, 1000, "credit", True)


def test_withdraw_amount_less_than_or_equal_zero():
    # Branch: amount <= 0 -> True
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 0, "savings", True)


def test_withdraw_amount_not_multiple_of_100():
    # Branch: amount > 0 is True, but amount % 100 != 0 -> True
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(10000, 150, "savings", True)


def test_withdraw_limit_exceeded():
    # Branch: amount > DAILY_LIMIT[account_type] -> True
    assert withdraw(50000, 30000, "savings", True) == "limit exceeded"


def test_withdraw_own_bank_success():
    # Branch: not own_bank -> False
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_withdraw_other_bank_low_amount():
    # Branch: not own_bank -> True, amount > 10000 -> False (fee = 20)
    assert withdraw(10000, 5000, "savings", False) == 4980


def test_withdraw_other_bank_high_amount():
    # Branch: not own_bank -> True, amount > 10000 -> True (fee = 20 + 10 = 30)
    assert withdraw(20000, 15000, "savings", False) == 4970


def test_withdraw_current_account_success():
    # Test current account within limit (50000)
    assert withdraw(60000, 40000, "current", True) == 20000


def test_withdraw_insufficient_funds():
    # Branch: amount + fee > balance -> True
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


# ---------------------------------------------------------
# Branch Coverage Tests for pin_check()
# ---------------------------------------------------------
def test_pin_check_attempts_greater_than_or_equal_3():
    # Branch: attempts >= 3 -> True
    assert pin_check(1234, 1234, 3) == "card blocked"
    assert pin_check(1234, 1234, 4) == "card blocked"


def test_pin_check_entered_equals_actual():
    # Branch: entered == actual -> True
    assert pin_check(1234, 1234, 0) == "ok"
    assert pin_check(1234, 1234, 2) == "ok"


def test_pin_check_last_attempt_failed():
    # Branch: entered != actual, attempts == 2 -> True
    assert pin_check(9999, 1234, 2) == "card blocked"


def test_pin_check_retry():
    # Branch: entered != actual, attempts != 2 (and < 3) -> True
    assert pin_check(9999, 1234, 0) == "retry"
    assert pin_check(9999, 1234, 1) == "retry"


# ---------------------------------------------------------
# Branch Coverage Tests for note_breakup()
# ---------------------------------------------------------
def test_note_breakup_invalid_amount():
    # Branch: amount % 100 != 0 -> True
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(250)


def test_note_breakup_remaining_greater_equal_200():
    # Branch: remaining >= 200 -> True
    # 800: 500*1, remaining 300 >= 200 -> 200*1, remaining 100 -> 100*1
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_remaining_less_than_200():
    # Branch: remaining >= 200 -> False (else: notes_200 = 0)
    # 600: 500*1, remaining 100 < 200 -> 200*0, 100*1
    assert note_breakup(600) == (1, 0, 1)
    # 500: remaining 0 < 200 -> 200*0, 100*0
    assert note_breakup(500) == (1, 0, 0)
