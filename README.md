# Lab 6: Code and Branch Coverage — ATM Withdrawal

**Student:** ABHIJNA MARATHE PES2UG24CS020
**Upstream Repo:** [SETAPESU26/L6_L7_18_atm_withdrawal](https://github.com/SETAPESU26/L6_L7_18_atm_withdrawal)

---

## About

This lab explores the difference between **statement (line) coverage** and **branch coverage** using a small Python ATM withdrawal module (`atm_withdrawal.py`).

The module simulates:
- **`withdraw()`** — processes ATM withdrawals with daily limits and inter-bank fees
- **`pin_check()`** — validates PIN entry and tracks failed attempts
- **`note_breakup()`** — calculates the denomination breakdown (₹500, ₹200, ₹100) for a given amount

---

## Files

| File | Description |
|------|-------------|
| `atm_withdrawal.py` | The module under test |
| `test_atm_withdrawal.py` | Starter test file (completed with all branch coverage tests) |
| `CodeCoverageTest_atm_withdrawal.py` | Test cases achieving **100% statement coverage** |
| `BranchCoverageTest_atm_withdrawal.py` | Test cases achieving **100% branch coverage** |
| `code_coverage_screenshot.png` | Terminal output for code coverage run |
| `branch_coverage_screenshot.png` | Terminal output for branch coverage run |

---

## Coverage Results

### Statement Coverage — 100%

```bash
coverage run -m pytest CodeCoverageTest_atm_withdrawal.py && coverage report -m
