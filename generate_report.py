from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.25)
    section.right_margin  = Inches(1)

# ── Helpers ─────────────────────────────────────────────────────────────────

def set_para_fmt(para, size=12, bold=False, italic=False,
                 align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                 space_before=0, space_after=6,
                 line_spacing=1.5):
    para.alignment = align
    pf = para.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = line_spacing
    for run in para.runs:
        run.font.name  = 'Times New Roman'
        run.font.size  = Pt(size)
        run.font.bold  = bold
        run.font.italic = italic

def add_heading(text, level=1):
    size   = 14 if level == 1 else (13 if level == 2 else 12)
    para   = doc.add_paragraph()
    run    = para.add_run(text)
    run.font.name  = 'Times New Roman'
    run.font.size  = Pt(size)
    run.font.bold  = True
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(12 if level == 1 else 8)
    pf.space_after  = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.5
    return para

def add_body(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    para = doc.add_paragraph()
    run  = para.add_run(text)
    run.font.name   = 'Times New Roman'
    run.font.size   = Pt(12)
    run.font.bold   = bold
    run.font.italic = italic
    para.alignment  = align
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after  = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.5
    return para

def add_bullet(text):
    para = doc.add_paragraph(style='List Bullet')
    run  = para.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after  = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.5
    return para

def add_figure_placeholder(num, caption):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(f'[ INSERT SCREENSHOT: Figure {num} ]')
    run.font.name   = 'Times New Roman'
    run.font.size   = Pt(11)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    pf = para.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after  = Pt(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.0

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = cap.add_run(f'Figure {num}. {caption}')
    cr.font.name = 'Times New Roman'
    cr.font.size = Pt(11)
    cr.font.bold = False
    pf2 = cap.paragraph_format
    pf2.space_before = Pt(0)
    pf2.space_after  = Pt(10)
    pf2.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf2.line_spacing      = 1.0

def add_table(headers, rows, table_num, caption):
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cr = cap.add_run(f'Table {table_num}. {caption}')
    cr.font.name = 'Times New Roman'
    cr.font.size = Pt(11)
    cr.font.bold = True
    pf = cap.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after  = Pt(3)

    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        for run in hdr_cells[i].paragraphs[0].runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = True
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for r_idx, row_data in enumerate(rows):
        cells = table.rows[r_idx+1].cells
        for c_idx, val in enumerate(row_data):
            cells[c_idx].text = val
            for run in cells[c_idx].paragraphs[0].runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(11)

    doc.add_paragraph()

def add_code(code_text):
    para = doc.add_paragraph()
    run  = para.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after  = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.0
    # Light grey background via shading
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F2F2F2')
    para._p.get_or_add_pPr().append(shd)
    return para

def page_break():
    doc.add_page_break()

def center_bold(text, size=12):
    para = doc.add_paragraph()
    run  = para.add_run(text)
    run.font.name  = 'Times New Roman'
    run.font.size  = Pt(size)
    run.font.bold  = True
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(6)
    pf.space_after  = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.5
    return para

def center_normal(text, size=12, bold=False):
    para = doc.add_paragraph()
    run  = para.add_run(text)
    run.font.name  = 'Times New Roman'
    run.font.size  = Pt(size)
    run.font.bold  = bold
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = para.paragraph_format
    pf.space_before = Pt(3)
    pf.space_after  = Pt(3)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.5
    return para

def blank(n=1):
    for _ in range(n):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after  = Pt(0)

# ════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ════════════════════════════════════════════════════════════════════

blank(3)
center_bold('MINOR PROJECT REPORT', 14)
center_normal('(Project Term January – May 2025)', 12)
blank(2)
center_bold('ONLINE EXAMINATION PLATFORM WITH AUTOMATED\nPROCTORING AND C CODE EVALUATION', 14)
blank(3)

# Submitted by / Under guidance table
table = doc.add_table(rows=1, cols=2)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
left  = table.cell(0, 0)
right = table.cell(0, 1)

def cell_para(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    if p.text:
        p = cell.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = bold
    p.alignment   = align
    return p

cell_para(left, 'Submitted by', bold=True)
cell_para(left, 'Inam Khan')
cell_para(left, 'Registration Number: _______________')
cell_para(left, 'Programme & Section: _______________')

cell_para(right, 'Under the Guidance of', bold=True)
cell_para(right, '_______________ (Faculty Name)')
cell_para(right, 'Designation: _______________')
cell_para(right, 'Department of CSE')

# Remove table borders
for row in table.rows:
    for cell in row.cells:
        for border in ['top','left','bottom','right']:
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_borders = OxmlElement('w:tcBorders')
            b = OxmlElement(f'w:{border}')
            b.set(qn('w:val'), 'none')
            tc_borders.append(b)
            tc_pr.append(tc_borders)

blank(2)
center_normal('Lovely Professional University, Phagwara')

page_break()

# ════════════════════════════════════════════════════════════════════
#  DECLARATION
# ════════════════════════════════════════════════════════════════════

add_heading('DECLARATION', 1)

add_body(
    'I hereby declare that the project work entitled "Online Examination Platform with Automated '
    'Proctoring and C Code Evaluation" is an authentic record of my own work carried out as '
    'requirements of Minor Project for the award of degree of _______________ (Programme Name) '
    'from Lovely Professional University, Phagwara, under the guidance of _______________ '
    '(Name of Faculty Mentor), during January–May 2025.'
)
blank()
add_body('(Signature of Student)', align=WD_ALIGN_PARAGRAPH.LEFT)
add_body('Inam Khan', bold=True)
add_body('Registration Number: _______________')
add_body('Date: ___________________')
blank()
add_body(
    'This is to certify that the above statement made by the student is correct to the best of my knowledge and belief.'
)
blank()
add_body('_______________ (Name, U.ID and Designation)')
add_body('Faculty Mentor')

page_break()

# ════════════════════════════════════════════════════════════════════
#  ACKNOWLEDGEMENT
# ════════════════════════════════════════════════════════════════════

add_heading('ACKNOWLEDGEMENT', 1)

add_body(
    'I would like to express my profound gratitude to Mrs./Dr. _______________ (HOD) of the '
    'Computer Science & Engineering department, and Dr. _______________ (HOS) of Lovely '
    'Professional University for their contributions to the completion of my project titled '
    '"Online Examination Platform with Automated Proctoring and C Code Evaluation".'
)
add_body(
    'I would like to express my special thanks to my mentor Mr./Mrs. _______________ for their '
    'time and efforts provided throughout the year. The useful advice and suggestions were really '
    'helpful during the project\'s completion. In this aspect, I am eternally grateful.'
)
add_body(
    'I would like to acknowledge that this project was completed entirely by me and not by someone else.'
)
blank()
add_body('Signature')
add_body('Inam Khan', bold=True)
add_body('Registration Number: _______________')

page_break()

# ════════════════════════════════════════════════════════════════════
#  TABLE OF CONTENTS
# ════════════════════════════════════════════════════════════════════

add_heading('TABLE OF CONTENTS', 1)

toc_data = [
    ('DESCRIPTION', 'PAGE NUMBER'),
    ('DECLARATION', 'iii'),
    ('ACKNOWLEDGEMENTS', 'iv'),
    ('LIST OF FIGURES', 'v'),
    ('LIST OF TABLES', 'vi'),
    ('1. PROFILE OF THE PROBLEM (INTRODUCTION)', '1'),
    ('    1.1  Introduction', '1'),
    ('    1.2  Objectives of the System', '2'),
    ('2. EXISTING SYSTEM', '3'),
    ('    2.1  Existing Software', '3'),
    ('    2.2  Drawbacks of Existing Systems', '4'),
    ('    2.3  What is New in the Proposed System', '4'),
    ('3. PROBLEM ANALYSIS', '5'),
    ('    3.1  Problem Definition', '5'),
    ('    3.2  Project Plan', '5'),
    ('4. SOFTWARE REQUIREMENT ANALYSIS', '6'),
    ('    4.1  General Description', '6'),
    ('    4.2  Functional Requirements', '6'),
    ('    4.3  Non-Functional Requirements', '7'),
    ('    4.4  Tools and Technologies', '8'),
    ('5. DESIGN', '9'),
    ('    5.1  DFD – Context and Level 1', '9'),
    ('    5.2  ER Diagram', '11'),
    ('    5.3  Database Table Design', '11'),
    ('6. IMPLEMENTATION', '14'),
    ('    6.1  Code Modules', '14'),
    ('    6.2  Screenshots of the Project', '20'),
    ('7. BIBLIOGRAPHY', '22'),
]

toc_table = doc.add_table(rows=len(toc_data), cols=2)
toc_table.style = 'Table Grid'
toc_table.alignment = WD_TABLE_ALIGNMENT.LEFT

for i, (desc, pg) in enumerate(toc_data):
    c0 = toc_table.cell(i, 0)
    c1 = toc_table.cell(i, 1)
    is_header = (i == 0)
    is_chapter = desc and desc[0].isdigit() and not desc.startswith(' ')

    for cell, text in [(c0, desc), (c1, pg)]:
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = is_header or is_chapter
        p.alignment   = WD_ALIGN_PARAGRAPH.LEFT if cell == c0 else WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()
page_break()

# ════════════════════════════════════════════════════════════════════
#  LIST OF FIGURES
# ════════════════════════════════════════════════════════════════════

add_heading('LIST OF FIGURES', 1)

add_table(
    ['FIGURE', 'TITLE', 'PAGE NUMBER'],
    [
        ('5.1', 'DFD Level 0 – Context Diagram', '9'),
        ('5.2', 'DFD Level 1 – Main System Processes', '10'),
        ('5.3', 'ER Diagram', '11'),
        ('6.1', 'Home Page', '20'),
        ('6.2', 'Student Dashboard', '20'),
        ('6.3', 'Exam Interface', '21'),
        ('6.4', 'Teacher Dashboard', '21'),
        ('6.5', 'Proctoring Snapshots View', '22'),
    ],
    'v', 'List of Figures'
)

page_break()

# ════════════════════════════════════════════════════════════════════
#  LIST OF TABLES
# ════════════════════════════════════════════════════════════════════

add_heading('LIST OF TABLES', 1)

add_table(
    ['TABLE', 'TITLE', 'PAGE NUMBER'],
    [
        ('2.1', 'Comparison of Existing Exam Platforms', '3'),
        ('4.1', 'Functional Requirements', '6'),
        ('4.2', 'Non-Functional Requirements', '7'),
        ('4.3', 'Tools and Technologies', '8'),
        ('5.1', 'UserRole Table', '11'),
        ('5.2', 'Exam Table', '12'),
        ('5.3', 'Question Table', '12'),
        ('5.4', 'StudentExam Table', '13'),
        ('5.5', 'Answer Table', '13'),
        ('5.6', 'ProctorSnapshot Table', '13'),
    ],
    'vi', 'List of Tables'
)

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 1
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 1: PROFILE OF THE PROBLEM (INTRODUCTION)', 1)
add_heading('1.1  Introduction', 2)

add_body(
    'The shift to online education has created a growing need for digital examination systems '
    'capable of handling programming-based assessments, automated grading, and academic integrity '
    'monitoring — all within a single platform. Existing free tools like Google Forms lack code '
    'execution support, while commercial platforms such as HackerRank and Codility are expensive '
    'and store student data on external servers, raising privacy and data sovereignty concerns.'
)
add_body(
    'This project — "Online Examination Platform with Automated Proctoring and C Code Evaluation" '
    '— is a self-hosted Django web application that enables teachers to create multi-type exams '
    '(MCQ, True/False, Short Answer, C Coding), automatically grades C language submissions using '
    'a local GCC compiler, and monitors student behaviour through webcam and screen proctoring '
    'with tab-switch detection. The entire system is built on free, open-source technologies '
    'with no dependency on external APIs or cloud services.'
)

add_heading('1.2  Objectives of the System', 2)

objectives = [
    'Build a dual-role (Teacher/Student) Django-based web application.',
    'Support four question types: MCQ, True/False, Short Answer, and C Coding.',
    'Auto-grade C code submissions by compiling and running against predefined test cases using local GCC.',
    'Implement real-time proctoring via periodic webcam and screen capture.',
    'Detect tab-switching and auto-submit the exam server-side after 3 violations.',
    'Provide OTP-based password reset for secure account recovery.',
    'Use only free, open-source technologies — no external API or licensing cost.',
]
for o in objectives:
    add_bullet(o)

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 2
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 2: EXISTING SYSTEM', 1)
add_heading('2.1  Existing Software', 2)

add_body(
    'Several platforms currently address online examination and coding assessment needs. '
    'The major tools in use are Google Forms, Moodle, HackerRank for Work, Codility, and '
    'ProctorU. Google Forms is free and widely used but supports only MCQ and short answer '
    'questions with no code execution capability. Moodle is an open-source LMS with a coding '
    'plugin (VPL), but requires complex server-side setup. HackerRank and Codility are '
    'commercial platforms that support coding assessment and proctoring but are subscription-based '
    'and store data externally. ProctorU is a dedicated proctoring service that transmits '
    'biometric data to third-party servers.'
)

add_table(
    ['Feature', 'Google Forms', 'Moodle', 'HackerRank', 'Our System'],
    [
        ('MCQ Support',          'Yes',      'Yes',       'Yes',       'Yes'),
        ('C Code Evaluation',    'No',       'Via Plugin', 'Yes',      'Yes'),
        ('Built-in Proctoring',  'No',       'No',        'Yes (paid)','Yes'),
        ('Tab-Switch Detection', 'No',       'No',        'Yes',       'Yes'),
        ('Self-Hosted / Free',   'Yes',      'Yes',       'No',        'Yes'),
        ('OTP Password Reset',   'No',       'No',        'No',        'Yes'),
    ],
    '2.1', 'Comparison of Existing Exam Platforms'
)

add_heading('2.2  Drawbacks of Existing Systems', 2)

add_bullet('Google Forms and standard LMS tools do not support live code execution.')
add_bullet('HackerRank and Codility are subscription-based; student data stored on external servers.')
add_bullet('Moodle requires significant expertise and plugin configuration for coding support.')
add_bullet('Dedicated proctoring services (ProctorU) transmit biometric data to third-party servers.')

add_heading('2.3  What is New in the Proposed System', 2)

add_bullet('Local GCC integration: C code compiled and executed server-side — no external API.')
add_bullet('Mixed question types: MCQ + Coding in a single exam paper.')
add_bullet('Hidden test cases: Students cannot reverse-engineer grading criteria.')
add_bullet('Data sovereignty: All snapshots and exam data stored in the institution\'s own database.')
add_bullet('Auto-submit on 3 tab-switches enforced server-side, not just client-side.')

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 3
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 3: PROBLEM ANALYSIS', 1)
add_heading('3.1  Problem Definition', 2)

add_body(
    'Design and implement a web-based examination platform that enables teachers to create '
    'mixed-type exams (MCQ, True/False, Short Answer, C Coding), automatically grades C '
    'code submissions using a local compiler, monitors student behaviour through proctoring, '
    'and provides post-exam result review — entirely self-hosted and open-source, with no '
    'recurring licensing cost.'
)

add_heading('3.2  Project Plan', 2)

add_table(
    ['Phase', 'Activity', 'Weeks'],
    [
        ('1',  'Requirement Analysis',              '1–2'),
        ('2',  'System Design (ER, DFD)',            '3–4'),
        ('3',  'Database Models & Migrations',      '5–6'),
        ('4',  'Auth Module (Login, OTP Reset)',    '6–7'),
        ('5',  'Teacher Module',                    '7–9'),
        ('6',  'Student & Exam Module',             '9–11'),
        ('7',  'C Code Execution Engine',           '10–12'),
        ('8',  'Proctoring Module',                 '12–13'),
        ('9',  'Testing & Bug Fix',                 '13–15'),
        ('10', 'Documentation',                     '15–16'),
    ],
    '3.1', 'Project Gantt Chart (16-week plan)'
)

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 4
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 4: SOFTWARE REQUIREMENT ANALYSIS', 1)
add_heading('4.1  General Description', 2)

add_body(
    'The system follows Django\'s Model-View-Template (MVT) pattern. It is structured as a '
    'single Django app (Examapp) containing all models, views, URL routes, and HTML templates. '
    'SQLite is used for development; PostgreSQL is supported for production deployment. Static '
    'files (CSS, JavaScript, images) are served using WhiteNoise middleware.'
)

add_heading('4.2  Functional Requirements', 2)

add_table(
    ['FR No.', 'Requirement'],
    [
        ('FR-01', 'Students self-register using name, reg. number, email, course, section, and password.'),
        ('FR-02', 'Teacher accounts are created only by the Django administrator.'),
        ('FR-03', 'Login requires role selection (student/teacher) and credential verification.'),
        ('FR-04', 'Password reset via 6-digit OTP sent to registered email (valid 10 minutes).'),
        ('FR-05', 'Teachers create exams with title, duration, start/end time, total/passing marks.'),
        ('FR-06', 'Teachers add questions of 4 types: MCQ, True/False, Short Answer, Coding (C).'),
        ('FR-07', 'Coding questions support test cases with stdin, expected output, marks, hidden flag.'),
        ('FR-08', 'Teachers assign students to exams and publish them.'),
        ('FR-09', 'Students view exams as: Upcoming / Available / Completed.'),
        ('FR-10', 'Exam interface shows countdown timer; answers auto-saved via AJAX on change.'),
        ('FR-11', 'C code compiled and executed locally; stdout matched against all test cases.'),
        ('FR-12', 'Webcam and screen snapshots captured every 30 seconds during exam.'),
        ('FR-13', 'On 3rd tab-switch, exam auto-submitted server-side with grades calculated.'),
        ('FR-14', 'Teachers review student answers and proctoring snapshots after exam.'),
    ],
    '4.1', 'Functional Requirements'
)

add_heading('4.3  Non-Functional Requirements', 2)

add_table(
    ['NFR No.', 'Category', 'Requirement'],
    [
        ('NFR-01', 'Security',      'Passwords stored as PBKDF2-SHA256 hashes. CSRF protection on all POST forms.'),
        ('NFR-02', 'Security',      'C code executes in an isolated temp directory deleted immediately after run.'),
        ('NFR-03', 'Performance',   'Compile timeout: 15 sec. Execution timeout: 5 sec. Memory limit: 64 MB.'),
        ('NFR-04', 'Reliability',   'AJAX auto-save prevents answer loss on accidental navigation or browser crash.'),
        ('NFR-05', 'Data Integrity','A submitted exam cannot be resubmitted (enforced server-side).'),
        ('NFR-06', 'Usability',     'Works on any modern browser — no plugin or installation required.'),
    ],
    '4.2', 'Non-Functional Requirements'
)

add_heading('4.4  Tools and Technologies', 2)

add_table(
    ['Category', 'Technology', 'Version'],
    [
        ('Programming Language', 'Python',          '3.10+'),
        ('Web Framework',        'Django',           '6.0.3'),
        ('Database (Dev)',        'SQLite',           '3.x'),
        ('Database (Prod)',       'PostgreSQL',       '15+'),
        ('Static Files',          'WhiteNoise',      '6.12.0'),
        ('WSGI Server',           'Gunicorn',        '25.3.0'),
        ('C Compiler',            'GCC / Clang',     'System'),
        ('Frontend',              'HTML5, CSS3, JS', '–'),
        ('Webcam API',            'MediaDevices API','Browser'),
        ('Version Control',       'Git',             '–'),
    ],
    '4.3', 'Tools and Technologies'
)

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 5
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 5: DESIGN', 1)
add_heading('5.1  Data Flow Diagrams (DFD)', 2)

add_body('Figure 5.1 – DFD Level 0 (Context Diagram)', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_code(
    'STUDENT ──► [ ONLINE EXAM PLATFORM ] ──► STUDENT (Results, Questions)\n'
    'TEACHER ──►                           ──► TEACHER (Results, Snapshots)'
)

add_body('Figure 5.2 – DFD Level 1 (Main Processes)', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_code(
    ' ┌─────────────────┐  ┌────────────────────┐  ┌───────────────────────┐\n'
    ' │ 1.0 AUTH        │  │ 2.0 EXAM MGMT      │  │ 3.0 EXAM ATTEMPT      │\n'
    ' │ Register/Login  │  │ Create/Edit Exam   │  │ Start / Answer / Save │\n'
    ' │ OTP Reset       │  │ Add Questions      │  │ Timer / Submit        │\n'
    ' └─────────────────┘  │ Assign Students    │  └──────────┬────────────┘\n'
    '                      └────────┬───────────┘             │\n'
    '                               └──────────────┬──────────┘\n'
    '                                     ┌─────────▼──────────────────────┐\n'
    '                                     │ 4.0 GRADING ENGINE             │\n'
    '                                     │ MCQ/TF→Auto | C→Local GCC     │\n'
    '                                     └─────────┬──────────────────────┘\n'
    '                                     ┌─────────▼──────────────────────┐\n'
    '                                     │ 5.0 PROCTORING                 │\n'
    '                                     │ Webcam + Screen + Tab-Switch   │\n'
    '                                     └────────────────────────────────┘'
)

add_heading('5.2  ER Diagram', 2)
add_body('Figure 5.3 – Entity-Relationship Diagram', bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_code(
    ' User ──1:1── UserRole\n'
    ' User ──1:N── Exam (as teacher)\n'
    ' User ──1:N── PasswordResetOTP\n'
    '\n'
    ' Exam ──1:N── Question ──1:N── Choice\n'
    '                        ──1:N── CodingTestCase\n'
    '\n'
    ' Exam ──1:N── StudentExam ──1:N── Answer\n'
    '                           ──1:N── ProctorSnapshot'
)

add_heading('5.3  Database Table Design', 2)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ('id',             'BigAutoField PK', 'Auto ID'),
        ('user_id',        'FK → User',       'Creator (teacher)'),
        ('role',           'VARCHAR(10)',      'student or teacher'),
        ('course',         'VARCHAR(100)',     'Student course name'),
        ('section',        'VARCHAR(50)',      'Student section'),
    ],
    '5.1', 'UserRole Table'
)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ('id',             'BigAutoField PK', 'Auto ID'),
        ('teacher_id',     'FK → User',       'Exam creator'),
        ('title',          'VARCHAR(200)',     'Exam title'),
        ('duration_minutes','Integer',         'Time allowed'),
        ('start_time',     'DateTime',         'Exam opens at'),
        ('end_time',       'DateTime',         'Exam closes at'),
        ('total_marks',    'Integer',          'Maximum marks (default 100)'),
        ('passing_marks',  'Integer',          'Passing threshold (default 40)'),
        ('is_published',   'Boolean',          'Visible to students'),
    ],
    '5.2', 'Exam Table'
)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ('id',             'BigAutoField PK', 'Auto ID'),
        ('exam_id',        'FK → Exam',       'Parent exam'),
        ('question_text',  'TextField',       'Question content'),
        ('question_type',  'VARCHAR(20)',     'mcq / true_false / short_answer / coding'),
        ('marks',          'Integer',         'Marks for this question'),
        ('order',          'Integer',         'Display sequence'),
    ],
    '5.3', 'Question Table'
)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ('id',               'BigAutoField PK','Auto ID'),
        ('student_id',       'FK → User',      'Student'),
        ('exam_id',          'FK → Exam',      'Assigned exam'),
        ('is_submitted',     'Boolean',        'Submission status'),
        ('obtained_marks',   'Integer (null)', 'Final marks scored'),
        ('tab_switch_count', 'Integer',        'Tab-switch violations'),
        ('exam_started_at',  'DateTime (null)','When student began'),
    ],
    '5.4', 'StudentExam Table'
)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ('id',               'BigAutoField PK','Auto ID'),
        ('student_exam_id',  'FK → StudentExam','Session'),
        ('question_id',      'FK → Question', 'Question answered'),
        ('selected_choice_id','FK (null)',     'For MCQ/TF'),
        ('written_answer',   'TextField',      'For Short Answer / Coding'),
        ('marks_obtained',   'Integer (null)', 'Marks awarded'),
    ],
    '5.5', 'Answer Table'
)

add_table(
    ['Column', 'Type', 'Description'],
    [
        ('id',              'BigAutoField PK','Auto ID'),
        ('student_exam_id', 'FK → StudentExam','Exam session'),
        ('snapshot_type',   'VARCHAR(10)',    'webcam or screen'),
        ('image_data',      'TextField',      'Base64-encoded JPEG'),
        ('is_flagged',      'Boolean',        'Flagged for teacher review'),
        ('captured_at',     'DateTime',       'Capture timestamp'),
    ],
    '5.6', 'ProctorSnapshot Table'
)

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 6 – IMPLEMENTATION
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 6: IMPLEMENTATION', 1)
add_heading('6.1  Code Modules', 2)

# --- Module 1 ---
add_heading('Module 1 – C Code Execution Engine (views.py)', 3)
add_code(
'''def _execute_c_code(code, stdin):
    """Compile and execute student C code locally using system GCC."""
    compiler   = getattr(django_settings, 'LOCAL_C_COMPILER', '/usr/bin/gcc')
    time_limit = getattr(django_settings, 'LOCAL_C_TIME_LIMIT', 5)
    work_dir   = tempfile.mkdtemp(prefix='exam_c_')
    src_path   = os.path.join(work_dir, 'solution.c')
    bin_path   = os.path.join(work_dir, 'solution')
    try:
        with open(src_path, 'w') as f:
            f.write(code)
        compile_proc = subprocess.run(
            [compiler, src_path, '-o', bin_path, '-lm'],
            capture_output=True, text=True, timeout=15,
        )
        if compile_proc.returncode != 0:
            return '', '', compile_proc.stderr, 6, 'Compilation Error'
        run_proc = subprocess.run(
            [bin_path], input=stdin or '',
            capture_output=True, text=True, timeout=time_limit,
        )
        if run_proc.returncode != 0:
            return run_proc.stdout, run_proc.stderr, '', 11, 'Runtime Error'
        return run_proc.stdout, run_proc.stderr, '', 3, 'Accepted'
    except subprocess.TimeoutExpired:
        return '', '', '', 5, 'Time Limit Exceeded'
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)  # always clean up'''
)

# --- Module 2 ---
add_heading('Module 2 – Tab-Switch Detection & Auto-Submit (views.py)', 3)
add_code(
'''@require_POST
@login_required(login_url='login')
def record_tab_switch(request, student_exam_id):
    student_exam = get_object_or_404(StudentExam, id=student_exam_id, student=request.user)
    student_exam.tab_switch_count += 1
    student_exam.total_suspicion_warnings += 1
    student_exam.save()
    if student_exam.tab_switch_count >= 3:
        total = 0
        for answer in student_exam.answers.all():
            q = answer.question
            if q.question_type in ['mcq', 'true_false']:
                if answer.selected_choice and answer.selected_choice.is_correct:
                    answer.marks_obtained = q.marks;  total += q.marks
                else:
                    answer.marks_obtained = 0
            elif q.question_type == 'coding':
                m, graded = _grade_coding_answer(q, answer.written_answer or '')
                if graded and m is not None:
                    answer.marks_obtained = m;  total += m
            answer.save()
        student_exam.obtained_marks = total
        student_exam.is_submitted   = True
        student_exam.submitted_at   = timezone.now()
        student_exam.save()
        return JsonResponse({'status': 'auto_submit',
                             'redirect_url': reverse('exam_result', args=[student_exam.id])})
    return JsonResponse({'status': 'recorded',
                         'tab_switch_count': student_exam.tab_switch_count})'''
)

# --- Module 3 ---
add_heading('Module 3 – OTP Password Reset (views.py)', 3)
add_code(
'''def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'auth/forgot_password.html',
                          {'error': 'No account found with this email.'})
        otp = f"{random.randint(100000, 999999)}"
        PasswordResetOTP.objects.create(user=user, otp=otp)
        send_mail(subject='Password Reset OTP - Exam Portal',
                  message=f'Your OTP: {otp}\\nValid for 10 minutes.',
                  from_email=None, recipient_list=[email])
        request.session['reset_user_id'] = user.id
        return redirect('verify_otp')
    return render(request, 'auth/forgot_password.html')'''
)

# --- Module 4 ---
add_heading('Module 4 – Proctoring Snapshot API (views.py)', 3)
add_code(
'''@require_POST
@login_required(login_url='login')
def save_snapshot(request, student_exam_id):
    student_exam = get_object_or_404(StudentExam, id=student_exam_id, student=request.user)
    data        = json.loads(request.body)
    image_b64   = data.get('image', '').strip()
    snap_type   = data.get('type', 'webcam')      # 'webcam' or 'screen'
    flag_reason = data.get('flag_reason', '')
    if not image_b64 or len(image_b64) < 100:
        return JsonResponse({'status': 'error'}, status=400)
    ProctorSnapshot.objects.create(
        student_exam=student_exam,
        snapshot_type=snap_type,
        image_data=image_b64,             # stored as base64 JPEG
        is_flagged=bool(flag_reason),
        flag_reason=flag_reason,
    )
    return JsonResponse({'status': 'saved'})'''
)

# --- Module 5 ---
add_heading('Module 5 – URL Configuration (urls.py)', 3)
add_code(
'''urlpatterns = [
    path('',                                                     views.home,               name='home'),
    path('signup/',                                              views.signup,             name='signup'),
    path('login/',                                               views.login_view,         name='login'),
    path('logout/',                                              views.logout_view,        name='logout'),
    path('forgot-password/',                                     views.forgot_password,    name='forgot_password'),
    path('verify-otp/',                                          views.verify_otp,         name='verify_otp'),
    path('reset-password/',                                      views.reset_password,     name='reset_password'),
    path('dashboard/',                                           views.dashboard,          name='dashboard'),
    path('teacher/dashboard/',                                   views.teacher_dashboard,  name='teacher_dashboard'),
    path('teacher/create-exam/',                                 views.create_exam,        name='create_exam'),
    path('teacher/exam/<int:exam_id>/edit/',                     views.edit_exam,          name='edit_exam'),
    path('teacher/exam/<int:exam_id>/questions/',                views.add_questions,      name='add_questions'),
    path('teacher/exam/<int:exam_id>/assign/',                   views.assign_students,    name='assign_students'),
    path('teacher/exam/<int:exam_id>/results/',                  views.exam_results,       name='exam_results'),
    path('student/dashboard/',                                   views.student_dashboard,  name='student_dashboard'),
    path('student/exam/<int:student_exam_id>/start/',            views.start_exam,         name='start_exam'),
    path('student/exam/<int:student_exam_id>/result/',           views.exam_result,        name='exam_result'),
    path('api/exam/<int:student_exam_id>/save-answer/<int:question_id>/', views.save_answer, name='save_answer'),
    path('api/exam/<int:student_exam_id>/tab-switch/',           views.record_tab_switch,  name='record_tab_switch'),
    path('api/exam/<int:student_exam_id>/submit/',               views.submit_exam,        name='submit_exam'),
    path('api/exam/<int:student_exam_id>/snapshot/',             views.save_snapshot,      name='save_snapshot'),
    path('api/code/run/',                                        views.run_code,           name='run_code'),
]'''
)

add_heading('6.2  Screenshots of the Project', 2)

screenshots = [
    ('6.1', 'Home Page – Landing screen with login/signup options'),
    ('6.2', 'Student Dashboard – Upcoming, Available, and Completed exam sections'),
    ('6.3', 'Exam Interface – Question panel, countdown timer, and C code editor'),
    ('6.4', 'Teacher Dashboard – Exam list with status, results, and actions'),
    ('6.5', 'Proctoring Snapshots – Webcam captures with flagged images highlighted'),
]

for num, cap in screenshots:
    add_figure_placeholder(num, cap)

page_break()

# ════════════════════════════════════════════════════════════════════
#  CHAPTER 7 – BIBLIOGRAPHY
# ════════════════════════════════════════════════════════════════════

add_heading('CHAPTER 7: BIBLIOGRAPHY', 1)

refs = [
    'Django Software Foundation. (2024). Django Documentation – Version 6.0. https://docs.djangoproject.com/en/6.0/',
    'Python Software Foundation. (2024). Python 3 Documentation. https://docs.python.org/3/',
    'WhiteNoise Project. (2024). WhiteNoise – Static file serving for Python web apps. https://whitenoise.readthedocs.io/',
    'Free Software Foundation. (2024). GCC, the GNU Compiler Collection. https://gcc.gnu.org/',
    'Mozilla Developer Network. (2024). MediaDevices.getUserMedia() API. https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia',
    'Mozilla Developer Network. (2024). Document: visibilitychange event. https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilitychange_event',
    'Sommerville, I. (2015). Software Engineering (10th ed.). Pearson Education.',
    'Pressman, R. S. & Maxim, B. R. (2019). Software Engineering: A Practitioner\'s Approach (9th ed.). McGraw-Hill.',
]

for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    run = p.add_run(f'{i}. {ref}')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    p.alignment   = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after  = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = 1.5

# ════════════════════════════════════════════════════════════════════
#  SAVE
# ════════════════════════════════════════════════════════════════════

doc.save(r'e:\Exam Platform\Minor_Project_Report.docx')
print('Done! Saved: Minor_Project_Report.docx')
