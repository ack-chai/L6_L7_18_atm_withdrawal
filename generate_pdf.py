import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "SETA Lab 7: Fuzzing for Input Validation Bugs")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "PES University — Dept of CSE")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 42, letter[0] - 54, 42)
        self.drawString(54, 30, "abhijna marathe | PES2UG24CS020")
        self.drawRightString(letter[0] - 54, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=8,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A202C")
    )

    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1A365D")
    )

    meta_val_style = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2D3748")
    )

    story = []

    # Title Banner
    story.append(Paragraph("LAB 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("Software Engineering: Testing and Automation (SETA) — Lab Submission", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=8))

    # Student Metadata Card
    meta_data = [
        [Paragraph("Student Name:", meta_label_style), Paragraph("abhijna marathe", meta_val_style),
         Paragraph("SRN:", meta_label_style), Paragraph("PES2UG24CS020", meta_val_style)],
        [Paragraph("Repository:", meta_label_style), Paragraph("SETAPESU26/L6_L7_18_atm_withdrawal", meta_val_style),
         Paragraph("Target Module:", meta_label_style), Paragraph("atm_withdrawal.py (Lab 7)", meta_val_style)]
    ]
    meta_table = Table(meta_data, colWidths=[90, 170, 90, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Objectives & Learning Outcomes
    story.append(Paragraph("1. Objective & Learning Outcomes", h1_style))
    story.append(Paragraph("<b>Objective:</b> To explore fuzz testing as a security and quality assurance technique by identifying and fixing bugs in the ATM withdrawal Python script using the Hypothesis property-based fuzzing library.", body_style))
    story.append(Paragraph("• <b>Understand Fuzz Testing:</b> Dynamic testing technique feeding unexpected, malformed data to discover crashes and security vulnerabilities.", bullet_style))
    story.append(Paragraph("• <b>Property-Based Fuzzing with Hypothesis:</b> Specify input strategies (<code>st.text() | st.none()</code>) to verify that functions never crash on unexpected inputs.", bullet_style))
    story.append(Paragraph("• <b>Detect and Fix Edge-Case Bugs:</b> Detect bugs like unhandled empty strings, null values, type mismatches, and zero divisions, and apply defensive programming to resolve them.", bullet_style))
    story.append(Spacer(1, 6))

    # Step 1: Installing dependencies
    story.append(Paragraph("2. Step 1: Installing Dependencies", h1_style))
    story.append(Paragraph("Installed testing and fuzzing frameworks: <code>pip install hypothesis pytest</code>.", body_style))
    sc_step1 = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots/ss_step1_install.png"
    if os.path.exists(sc_step1):
        story.append(RLImage(sc_step1, width=6.2*inch, height=1.35*inch))
    story.append(Spacer(1, 8))

    # Step 2: Run Buggy Application
    story.append(Paragraph("3. Step 2: Execution of Buggy Application", h1_style))
    story.append(Paragraph("Running <code>atm_withdrawal.py</code> with standard happy-path inputs (amount '2,500', card '1234 5678 9012 3456', CSV '500,1000,2000'). While valid inputs succeed, the implementation lacks input validation and crashes on edge cases.", body_style))
    sc_step2 = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots/ss_step2_buggy_run.png"
    if os.path.exists(sc_step2):
        story.append(RLImage(sc_step2, width=6.2*inch, height=2.1*inch))
    
    # Page Break to start Fuzz testing section cleanly
    story.append(PageBreak())

    # Step 3 & 4: Hypothesis Fuzz Testing & Failures
    story.append(Paragraph("4. Step 3: Fuzz Test Implementation using Hypothesis", h1_style))
    story.append(Paragraph("Hypothesis fuzz tests were added to <code>test_atm_withdrawal.py</code> using <code>@given(st.text() | st.none())</code> to assert that functions do not crash on arbitrary input strings or nulls:", body_style))
    
    test_code_text = (
        "from hypothesis import given, strategies as st\n"
        "from atm_withdrawal import notes_needed, mask_card, average_withdrawal\n\n"
        "@given(st.text() | st.none())\n"
        "def test_notes_needed_no_crash(s):\n"
        "    try:\n"
        "        notes_needed(s)\n"
        "    except Exception as e:\n"
        "        assert False, f\"notes_needed crashed with: {e}\"\n\n"
        "@given(st.text() | st.none())\n"
        "def test_mask_card_no_crash(s):\n"
        "    try:\n"
        "        mask_card(s)\n"
        "    except Exception as e:\n"
        "        assert False, f\"mask_card crashed with: {e}\"\n\n"
        "@given(st.text() | st.none())\n"
        "def test_average_withdrawal_no_crash(s):\n"
        "    try:\n"
        "        average_withdrawal(s)\n"
        "    except Exception as e:\n"
        "        assert False, f\"average_withdrawal crashed with: {e}\""
    )
    c_table = Table([[Paragraph(test_code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[480])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(c_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Step 4: Running Pytest and Detecting Fuzzing Failures", h1_style))
    story.append(Paragraph("Running <code>pytest test_atm_withdrawal.py</code> immediately triggered and minimized multiple crashes in all 3 functions:", body_style))
    story.append(Paragraph("• <code>notes_needed</code>: Crashed with <code>ValueError: invalid literal for int()</code> on <code>s=''</code> and <code>AttributeError</code> on <code>s=None</code>.", bullet_style))
    story.append(Paragraph("• <code>mask_card</code>: Crashed with <code>IndexError: list index out of range</code> on <code>s=''</code> and <code>AttributeError</code> on <code>s=None</code>.", bullet_style))
    story.append(Paragraph("• <code>average_withdrawal</code>: Crashed with <code>ValueError</code> on <code>s=''</code>, <code>ZeroDivisionError</code> on empty list, and <code>AttributeError</code> on <code>s=None</code>.", bullet_style))
    story.append(Spacer(1, 4))

    sc_step4 = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots/ss_step4_pytest_failing.png"
    if os.path.exists(sc_step4):
        story.append(RLImage(sc_step4, width=6.2*inch, height=3.5*inch))
    
    # Page Break for Step 5 & 6
    story.append(PageBreak())

    # Step 5: Hardening the Application
    story.append(Paragraph("6. Step 5: Hardening the Application Against Edge Cases", h1_style))
    story.append(Paragraph("The application was hardened with defensive programming techniques to handle all unforeseen inputs:", body_style))
    story.append(Paragraph("• <b>notes_needed:</b> Added type verification (<code>isinstance(amount, str)</code> and null checks). Strips commas and whitespace, catches non-numeric inputs gracefully returning <code>0</code>, and ensures non-negative results.", bullet_style))
    story.append(Paragraph("• <b>mask_card:</b> Verifies string presence. Checks token group count (<code>len(groups) &gt;= 4</code>) before accessing index 3, and supports contiguous card numbers. Returns safe fallback (<code>'XXXX XXXX XXXX XXXX'</code>) on invalid format.", bullet_style))
    story.append(Paragraph("• <b>average_withdrawal:</b> Parses comma-separated tokens individually with a <code>try-except</code> block. Ignores malformed values and prevents <code>ZeroDivisionError</code> by verifying <code>if not amounts: return 0</code>.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Output of Fixed Application (Step 5 Screenshot):</b>", h2_style))
    sc_step5 = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots/ss_step5_fixed_run.png"
    if os.path.exists(sc_step5):
        story.append(RLImage(sc_step5, width=6.2*inch, height=2.1*inch))
    story.append(Spacer(1, 8))

    # Step 6: Pytest Passing
    story.append(Paragraph("7. Step 6: Re-Running Fuzz Tests (All Tests Passed)", h1_style))
    story.append(Paragraph("Running <code>pytest -v test_atm_withdrawal.py</code> against the hardened application. Hypothesis generated hundreds of random Unicode strings, boundary conditions, and nulls with <b>0 failures</b> (100% test pass rate).", body_style))
    story.append(Spacer(1, 4))
    sc_step6 = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/screenshots/ss_step6_pytest_passing.png"
    if os.path.exists(sc_step6):
        story.append(RLImage(sc_step6, width=6.2*inch, height=1.9*inch))
    
    # Page Break for Code Appendix
    story.append(PageBreak())

    # Appendix: Source Code
    story.append(Paragraph("8. Appendix: Complete Code Listings", h1_style))
    
    story.append(Paragraph("<b>A. Fixed Application Script (<code>Lab 7/atm_withdrawal.py</code>):</b>", h2_style))
    with open("/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/Lab 7/atm_withdrawal.py", "r") as f:
        atm_code = f.read()
    app_table = Table([[Paragraph(atm_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[480])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(app_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>B. Fuzz Testing Suite (<code>Lab 7/test_atm_withdrawal.py</code>):</b>", h2_style))
    with open("/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/Lab 7/test_atm_withdrawal.py", "r") as f:
        test_code = f.read()
    test_table = Table([[Paragraph(test_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[480])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(test_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated clean PDF report: {filename}")

if __name__ == "__main__":
    pdf_path = "/Users/abhijna/.gemini/antigravity/scratch/lab7_fuzzing/Lab7_Fuzzing_Report_PES2UG24CS020.pdf"
    build_pdf(pdf_path)
