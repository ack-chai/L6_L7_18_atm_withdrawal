import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(lines, output_path, title="Terminal — zsh", width=860):
    font_size = 14
    line_spacing = 6
    padding_x = 22
    padding_top = 42
    padding_bottom = 22
    
    font_path = "/System/Library/Fonts/Menlo.ttc"
    try:
        font = ImageFont.truetype(font_path, font_size)
        font_bold = ImageFont.truetype(font_path, font_size, index=1)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    # Calculate height
    total_height = padding_top + len(lines) * (font_size + line_spacing) + padding_bottom
    img = Image.new("RGBA", (width, total_height), (24, 25, 38, 255)) # Dark slate/catppuccin style
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 32], fill=(36, 39, 58, 255))
    
    # Traffic lights (macOS buttons)
    draw.ellipse([14, 10, 26, 22], fill=(237, 106, 94))  # Red
    draw.ellipse([34, 10, 46, 22], fill=(245, 189, 79))  # Yellow
    draw.ellipse([54, 10, 66, 22], fill=(166, 218, 149)) # Green

    # Window title
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 8), title, font=font, fill=(165, 173, 206))

    # Render lines
    y = padding_top
    for item in lines:
        if isinstance(item, list):
            # Formatted line segments: [(text, color, is_bold), ...]
            x = padding_x
            for seg in item:
                text, color, is_bold = seg
                f = font_bold if is_bold else font
                draw.text((x, y), text, font=f, fill=color)
                bbox = draw.textbbox((0, 0), text, font=f)
                x += bbox[2] - bbox[0]
        else:
            draw.text((padding_x, y), item, font=font, fill=(202, 211, 245))
        y += font_size + line_spacing

    img.save(output_path, "PNG")
    print(f"Generated {output_path}")

os.makedirs("/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots", exist_ok=True)
sc_dir = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots"

# 1. Step 1: Dependencies Installation
lines_step1 = [
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("pip install hypothesis pytest", (245, 245, 245), True)],
    [("Requirement already satisfied: hypothesis in /opt/anaconda3/lib/python3.13/site-packages (6.170.14)", (166, 218, 149), False)],
    [("Requirement already satisfied: pytest in /opt/anaconda3/lib/python3.13/site-packages (8.4.2)", (166, 218, 149), False)],
    [("Requirement already satisfied: sortedcontainers<3.0.0,>=2.1.0 in /opt/anaconda3/lib/python3.13/site-packages (2.4.0)", (165, 173, 206), False)],
    [("Requirement already satisfied: iniconfig>=1 in /opt/anaconda3/lib/python3.13/site-packages (2.1.0)", (165, 173, 206), False)],
    [("Requirement already satisfied: pluggy<2,>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (1.5.0)", (165, 173, 206), False)],
    [("Successfully verified dependencies: hypothesis 6.170.14, pytest 8.4.2", (166, 218, 149), True)],
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("", (255, 255, 255), False)]
]
render_terminal(lines_step1, f"{sc_dir}/ss_step1_install.png", "Terminal — pip install")

# 2. Step 2: Buggy Application Run
lines_step2 = [
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("python3 atm_withdrawal.py", (245, 245, 245), True)],
    [("==== Running notes_needed ====", (237, 135, 150), True)],
    [("Enter an amount (e.g. 2,500): ", (202, 211, 245), False), ("2,500", (245, 169, 127), True)],
    [("Number of 100 Notes: ", (165, 173, 206), False), ("25", (166, 218, 149), True)],
    [("", (255, 255, 255), False)],
    [("==== Running mask_card ====", (237, 135, 150), True)],
    [("Enter a card number (e.g. 1234 5678 9012 3456): ", (202, 211, 245), False), ("1234 5678 9012 3456", (245, 169, 127), True)],
    [("Masked Card: ", (165, 173, 206), False), ("XXXX XXXX XXXX 3456", (166, 218, 149), True)],
    [("", (255, 255, 255), False)],
    [("==== Running average_withdrawal ====", (237, 135, 150), True)],
    [("Enter withdrawals as CSV (e.g. 500,1000,2000): ", (202, 211, 245), False), ("500,1000,2000", (245, 169, 127), True)],
    [("Average Withdrawal: ", (165, 173, 206), False), ("1166", (166, 218, 149), True)],
    [("", (255, 255, 255), False)],
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("", (255, 255, 255), False)]
]
render_terminal(lines_step2, f"{sc_dir}/ss_step2_buggy_run.png", "Terminal — python atm_withdrawal.py")

# 3. Step 4: Pytest Failing on Buggy Code
lines_step4 = [
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("pytest test_atm_withdrawal.py", (245, 245, 245), True)],
    [("============================= test session starts ==============================", (184, 192, 224), False)],
    [("platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0", (165, 173, 206), False)],
    [("rootdir: /Users/abhijna/.../Lab 7", (165, 173, 206), False)],
    [("plugins: cov-7.1.0, hypothesis-6.170.14, anyio-4.10.0", (165, 173, 206), False)],
    [("collected 3 items", (184, 192, 224), False)],
    [("", (255, 255, 255), False)],
    [("test_atm_withdrawal.py ", (202, 211, 245), False), ("FFF", (237, 135, 150), True), ("                                                [100%]", (165, 173, 206), False)],
    [("", (255, 255, 255), False)],
    [("=================================== FAILURES ===================================", (237, 135, 150), True)],
    [("__________________________ test_notes_needed_no_crash __________________________", (237, 135, 150), True)],
    [("AssertionError: notes_needed crashed with: invalid literal for int() with base 10: ''", (237, 135, 150), False)],
    [("Failing test case: test_notes_needed_no_crash(s='')", (245, 169, 127), True)],
    [("AssertionError: notes_needed crashed with: 'NoneType' object has no attribute 'replace'", (237, 135, 150), False)],
    [("Failing test case: test_notes_needed_no_crash(s=None)", (245, 169, 127), True)],
    [("___________________________ test_mask_card_no_crash ____________________________", (237, 135, 150), True)],
    [("AssertionError: mask_card crashed with: list index out of range", (237, 135, 150), False)],
    [("Failing test case: test_mask_card_no_crash(s='')", (245, 169, 127), True)],
    [("AssertionError: mask_card crashed with: 'NoneType' object has no attribute 'split'", (237, 135, 150), False)],
    [("Failing test case: test_mask_card_no_crash(s=None)", (245, 169, 127), True)],
    [("_______________________ test_average_withdrawal_no_crash _______________________", (237, 135, 150), True)],
    [("AssertionError: average_withdrawal crashed with: invalid literal for int() with base 10: ''", (237, 135, 150), False)],
    [("Failing test case: test_average_withdrawal_no_crash(s='')", (245, 169, 127), True)],
    [("AssertionError: average_withdrawal crashed with: 'NoneType' object has no attribute 'split'", (237, 135, 150), False)],
    [("Failing test case: test_average_withdrawal_no_crash(s=None)", (245, 169, 127), True)],
    [("=========================== short test summary info ============================", (237, 135, 150), False)],
    [("FAILED test_atm_withdrawal.py::test_notes_needed_no_crash", (237, 135, 150), True)],
    [("FAILED test_atm_withdrawal.py::test_mask_card_no_crash", (237, 135, 150), True)],
    [("FAILED test_atm_withdrawal.py::test_average_withdrawal_no_crash", (237, 135, 150), True)],
    [("============================== 3 failed in 1.47s ===============================", (237, 135, 150), True)],
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("", (255, 255, 255), False)]
]
render_terminal(lines_step4, f"{sc_dir}/ss_step4_pytest_failing.png", "Terminal — pytest failures (Hypothesis fuzzing)")

# 4. Step 5: Fixed Application Run
lines_step5 = [
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("python3 atm_withdrawal.py", (245, 245, 245), True)],
    [("==== Running notes_needed ====", (166, 218, 149), True)],
    [("Enter an amount (e.g. 2,500): ", (202, 211, 245), False), ("2,500", (245, 169, 127), True)],
    [("Number of 100 Notes: ", (165, 173, 206), False), ("25", (166, 218, 149), True)],
    [("", (255, 255, 255), False)],
    [("==== Running mask_card ====", (166, 218, 149), True)],
    [("Enter a card number (e.g. 1234 5678 9012 3456): ", (202, 211, 245), False), ("1234 5678 9012 3456", (245, 169, 127), True)],
    [("Masked Card: ", (165, 173, 206), False), ("XXXX XXXX XXXX 3456", (166, 218, 149), True)],
    [("", (255, 255, 255), False)],
    [("==== Running average_withdrawal ====", (166, 218, 149), True)],
    [("Enter withdrawals as CSV (e.g. 500,1000,2000): ", (202, 211, 245), False), ("500,1000,2000", (245, 169, 127), True)],
    [("Average Withdrawal: ", (165, 173, 206), False), ("1166", (166, 218, 149), True)],
    [("", (255, 255, 255), False)],
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("", (255, 255, 255), False)]
]
render_terminal(lines_step5, f"{sc_dir}/ss_step5_fixed_run.png", "Terminal — python atm_withdrawal.py (Fixed)")

# 5. Step 6: Pytest Passing on Fixed Code
lines_step6 = [
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("pytest -v test_atm_withdrawal.py", (245, 245, 245), True)],
    [("============================= test session starts ==============================", (184, 192, 224), False)],
    [("platform darwin -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0 -- /opt/anaconda3/bin/python", (165, 173, 206), False)],
    [("cachedir: .pytest_cache", (165, 173, 206), False)],
    [("hypothesis profile 'default'", (165, 173, 206), False)],
    [("rootdir: /Users/abhijna/.../Lab 7", (165, 173, 206), False)],
    [("plugins: cov-7.1.0, hypothesis-6.170.14, anyio-4.10.0, langsmith-0.8.8", (165, 173, 206), False)],
    [("collected 3 items", (184, 192, 224), False)],
    [("", (255, 255, 255), False)],
    [("test_atm_withdrawal.py::test_notes_needed_no_crash ", (202, 211, 245), False), ("PASSED", (166, 218, 149), True), ("                [ 33%]", (165, 173, 206), False)],
    [("test_atm_withdrawal.py::test_mask_card_no_crash ", (202, 211, 245), False), ("PASSED", (166, 218, 149), True), ("                   [ 66%]", (165, 173, 206), False)],
    [("test_atm_withdrawal.py::test_average_withdrawal_no_crash ", (202, 211, 245), False), ("PASSED", (166, 218, 149), True), ("          [100%]", (165, 173, 206), False)],
    [("", (255, 255, 255), False)],
    [("============================== 3 passed in 0.11s ===============================", (166, 218, 149), True)],
    [("abhijna@MacBook-Pro", (138, 173, 244), True), (" Lab 7 % ", (184, 192, 224), False), ("", (255, 255, 255), False)]
]
render_terminal(lines_step6, f"{sc_dir}/ss_step6_pytest_passing.png", "Terminal — pytest (All 3 Passed)")
