Lab 6: Code and Branch Coverage — ATM Withdrawal
Student: ABHIJNA MARATHE 
SRN PES2UG24CS020
Upstream Repo: SETAPESU26/L6_L7_18_atm_withdrawal

About
This lab explores the difference between statement (line) coverage and branch coverage using a small Python ATM withdrawal module (atm_withdrawal.py).

The module simulates:

withdraw() — processes ATM withdrawals with daily limits and inter-bank fees
pin_check() — validates PIN entry and tracks failed attempts
note_breakup() — calculates the denomination breakdown (₹500, ₹200, ₹100) for a given amount
Files
File	Description
atm_withdrawal.py	The module under test
test_atm_withdrawal.py	Starter test file (completed with all branch coverage tests)
CodeCoverageTest_atm_withdrawal.py	Test cases achieving 100% statement coverage
BranchCoverageTest_atm_withdrawal.py	Test cases achieving 100% branch coverage
code_coverage_screenshot.png	Terminal output for code coverage run
branch_coverage_screenshot.png	Terminal output for branch coverage run
Coverage Results
Statement Coverage — 100%
coverage run -m pytest CodeCoverageTest_atm_withdrawal.py && coverage report -m
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
atm_withdrawal.py                       34      0   100%
------------------------------------------------------------------
TOTAL                                   65      0   100%
Code Coverage Screenshot

Branch Coverage — 100% (22/22 branches)
coverage run --branch -m pytest BranchCoverageTest_atm_withdrawal.py && coverage report -m
Name                                   Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------------
atm_withdrawal.py                         34      0     22      0   100%
----------------------------------------------------------------------------------
TOTAL                                     76      0     22      0   100%
Branch Coverage Screenshot

Key Insight: Why Line Coverage ≠ Branch Coverage
Even with 100% statement coverage, branch coverage exposed a gap:

In withdraw():

if not own_bank:
    fee = 20
    if amount > 10000:   # ← this branch was only tested for amount > 10000
        fee += 10
The statement coverage tests always used amount > 10000 when own_bank=False, so line 15 (fee += 10) was executed. However, the else path (where own_bank=False but amount <= 10000) was never tested, which branch coverage caught.

How to Run
# Clone
git clone https://github.com/ack-chai/L6_L7_18_atm_withdrawal.git
cd L6_L7_18_atm_withdrawal/"Lab 6"

# Statement coverage
coverage run -m pytest CodeCoverageTest_atm_withdrawal.py
coverage report -m

# Branch coverage
coverage run --branch -m pytest BranchCoverageTest_atm_withdrawal.py
coverage report -m
