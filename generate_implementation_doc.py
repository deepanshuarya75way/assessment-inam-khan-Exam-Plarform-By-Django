from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins (tight to fit 5 pages) ───────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Cm(1.8)
section.bottom_margin = Cm(1.8)
section.left_margin   = Cm(2.2)
section.right_margin  = Cm(2.2)

INDIGO = RGBColor(0x63, 0x66, 0xF1)
DARK   = RGBColor(0x1E, 0x1B, 0x4B)
GRAY   = RGBColor(0x64, 0x74, 0x8B)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BODY   = RGBColor(0x1E, 0x29, 0x3B)

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(13); r.font.color.rgb = INDIGO
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = DARK
    return p

def body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.size = Pt(9.5); r.font.color.rgb = BODY
    return p

def bul(text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent  = Cm(0.5 + level * 0.4)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    r = p.add_run(text)
    r.font.size = Pt(9.5); r.font.color.rgb = BODY
    return p

def num(text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent  = Cm(0.5)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(1)
    r = p.add_run(text)
    r.font.size = Pt(9.5); r.font.color.rgb = BODY
    return p

def code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(0.6)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), "F1F5F9")
    pPr.append(shd)
    r = p.add_run(text)
    r.font.name = "Courier New"; r.font.size = Pt(8.5); r.font.color.rgb = BODY
    return p

def table(headers, rows, col_widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.style = "Table Grid"
    hdr = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        set_cell_bg(hdr[i], "6366F1")
        hdr[i].paragraphs[0].runs[0].font.color.rgb = WHITE
        hdr[i].paragraphs[0].runs[0].bold = True
        hdr[i].paragraphs[0].runs[0].font.size = Pt(9)
    for row_data in rows:
        row = tbl.add_row().cells
        for i, val in enumerate(row_data):
            row[i].text = val
            row[i].paragraphs[0].runs[0].font.size = Pt(9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(0)
title.paragraph_format.space_after  = Pt(2)
r = title.add_run("Online C-Programming Exam Platform")
r.bold = True; r.font.size = Pt(18); r.font.color.rgb = DARK

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.paragraph_format.space_after = Pt(8)
r2 = sub.add_run("Implementation Steps — Django 6.0  |  Python 3.x  |  SQLite")
r2.font.size = Pt(10); r2.font.color.rgb = INDIGO; r2.bold = True

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — OVERVIEW & STACK
# ══════════════════════════════════════════════════════════════════════════════
h1("1.  Project Overview")
body("A full-stack Django web application for online C-programming exams with automated grading and live proctoring. Two roles: Teacher and Student.")
table(
    ["Feature", "Details"],
    [
        ("Question Types",     "MCQ, True/False, Short Answer, C-Coding"),
        ("Auto-Grading",       "MCQ/T-F instantly; Coding via local GCC; Short Answer manual"),
        ("Proctoring",         "Webcam snapshots every 60s + tab-switch detection"),
        ("Code Execution",     "Local GCC/Clang compilation with 5s timeout"),
        ("Auth",               "Django session auth + OTP password reset"),
        ("Tech Stack",         "Django 6.0, SQLite (dev), PostgreSQL (prod), WhiteNoise, Gunicorn"),
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — SETUP & INSTALLATION
# ══════════════════════════════════════════════════════════════════════════════
h1("2.  Environment Setup & Installation")

h2("Prerequisites")
bul("Python 3.10+  |  GCC/MinGW installed and added to PATH  |  Git")

h2("Step-by-Step")
num("Clone the project:  git clone <repo-url>  then  cd \"Exam Platform\"")
num("Create virtual environment:  python -m venv venv  then activate it")
num("Install dependencies:  pip install -r requirements.txt")
num("Set GCC path in  Exam/settings.py:  LOCAL_C_COMPILER = 'C:/MinGW/bin/gcc.exe'")
num("Apply migrations:  python manage.py migrate")
num("Create superuser:  python manage.py createsuperuser")
num("Run server:  python manage.py runserver  →  open http://127.0.0.1:8000")

body("Key packages: Django 6.0.3, whitenoise 6.12, django-sslserver 0.22, gunicorn 25.3, psycopg2-binary (PostgreSQL).")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — PROJECT STRUCTURE & MODELS
# ══════════════════════════════════════════════════════════════════════════════
h1("3.  Project Structure & Database Models")

h2("Directory Layout")
code("Exam Platform/\n├── Exam/           → settings.py, urls.py, wsgi.py\n├── Examapp/        → models.py, views.py, urls.py, admin.py\n│   └── templates/  → base.html, auth/, teacher/, student/\n├── db.sqlite3\n└── requirements.txt")

h2("Database Models (Examapp/models.py)")
table(
    ["Model", "Purpose", "Key Fields"],
    [
        ("UserRole",        "Extends User with role info",         "role (student/teacher), course, section"),
        ("Exam",            "Exam metadata created by teacher",     "title, duration_minutes, start_time, end_time, total_marks, is_published"),
        ("Question",        "Single question in an exam",           "question_type (mcq/true_false/short_answer/coding), marks, order"),
        ("Choice",          "Answer options for MCQ/T-F",           "choice_text, is_correct, order"),
        ("CodingTestCase",  "Test cases for C coding questions",    "stdin, expected_output, marks, is_hidden"),
        ("StudentExam",     "Student's attempt record",             "student, exam, obtained_marks, tab_switch_count, is_submitted"),
        ("Answer",          "One answer per question per attempt",  "selected_choice, written_answer, is_correct, marks_obtained"),
        ("ProctorSnapshot", "Webcam images during exam",            "image_data (base64), is_flagged, flag_reason, captured_at"),
        ("PasswordResetOTP","OTP for password recovery",            "otp, created_at, is_used, is_expired() method"),
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — AUTHENTICATION & ROLES
# ══════════════════════════════════════════════════════════════════════════════
h1("4.  Authentication & User Roles")

h2("Student Registration  (/signup/)")
num("Student fills: name, reg number, email, password, course, section.")
num("View creates Django User + UserRole(role='student') and auto-logs in.")

h2("Login  (/login/)")
num("User enters credentials + selects role (student/teacher).")
num("After authenticate(), role is verified against UserRole.role.")
num("Redirects to /student/dashboard/ or /teacher/dashboard/ accordingly.")

h2("OTP Password Reset  (/forgot-password/ → /verify-otp/ → /reset-password/)")
num("6-digit OTP generated and emailed (printed to console in dev).")
num("OTP expires in 10 minutes. Marked is_used=True after use.")

h2("Role Enforcement")
bul("@login_required decorator on all protected views.")
bul("Teacher views check user.userrole.role == 'teacher', else redirect.")
bul("Teachers can only be created by the Admin — no self-registration.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — TEACHER PORTAL
# ══════════════════════════════════════════════════════════════════════════════
h1("5.  Teacher Portal")

h2("Create Exam  (/teacher/create-exam/)")
body("Teacher fills: title, description, duration, start/end time, total marks, passing marks. Creates Exam with is_published=False.")

h2("Add Questions  (/teacher/exam/<id>/questions/)")
table(
    ["Type", "Implementation"],
    [
        ("MCQ",          "Question + 4 choices, one marked is_correct=True"),
        ("True/False",   "Question + auto-generated True/False choices"),
        ("Short Answer", "Question text only; teacher grades manually later"),
        ("Coding (C)",   "Question + test cases: stdin, expected_output, marks, is_hidden flag"),
    ]
)

h2("Assign Students  (/teacher/exam/<id>/assign/)")
body("Checkbox list of all students. On submit: creates StudentExam records (unique_together prevents duplicates) and sets is_published=True.")

h2("Results & Review")
bul("/teacher/exam/<id>/results/ — table of all student scores (pass/fail)")
bul("/teacher/student-exam/<id>/review/ — per-question answer review with correct answers highlighted")
bul("/teacher/student-exam/<id>/snapshots/ — grid of webcam images, filterable by flagged/normal")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — STUDENT PORTAL
# ══════════════════════════════════════════════════════════════════════════════
h1("6.  Student Portal")

h2("Dashboard  (/student/dashboard/)")
table(
    ["Category", "Condition", "Action"],
    [
        ("Upcoming",   "start_time > now",                         "Countdown timer shown"),
        ("Available",  "start_time ≤ now ≤ end_time, not submitted","Start Exam button"),
        ("Completed",  "is_submitted = True",                      "View Result button"),
    ]
)

h2("Exam Interface  (/student/exam/<id>/start/)")
bul("Layout: 260px sidebar (timer, question nav grid, camera preview) + main question area.")
bul("Effective end time = min(exam.end_time, exam_started_at + duration_minutes).")
bul("Answers auto-saved every 30s and on question navigation via AJAX.")
bul("Coding questions: split-pane with CodeMirror (C syntax, Dracula theme) + Run Code button.")
bul("Auto-submit: timer reaches zero  OR  3rd tab switch  OR  manual submit.")

h2("Result  (/student/exam/<id>/result/)")
bul("Pass/Fail banner, score card, per-question breakdown with correct answers.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — GRADING & CODE EXECUTION
# ══════════════════════════════════════════════════════════════════════════════
h1("7.  Exam Grading & C Code Execution")

h2("Auto-Grading on Submission")
table(
    ["Question Type", "Grading Method"],
    [
        ("MCQ / True-False", "selected_choice.is_correct == True → full marks, else 0"),
        ("Short Answer",     "Skipped — teacher assigns marks manually via review page"),
        ("Coding (C)",       "Compile + run against all test cases; sum marks of passing cases"),
    ]
)

h2("C Code Execution Flow  (/api/code/run/ and grading)")
num("Write student code to a temp .c file.")
num("Compile:  gcc -o <binary> <source> -lm  (captures stderr for compile errors).")
num("Run binary with test case stdin; capture stdout with 5-second timeout.")
num("Compare stdout to expected_output (stripped whitespace).")
num("Return/store result code: 3=Accepted, 5=TLE, 6=Compile Error, 11=Runtime Error.")

body("WARNING: For production, wrap execution in a Docker container to prevent privilege escalation.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — PROCTORING SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
h1("8.  Proctoring System")

h2("Webcam Snapshots")
num("getUserMedia({video:true}) requests camera on exam load.")
num("Canvas captures frame every 60s → toDataURL('image/jpeg', 0.6) → base64.")
num("POSTed to /api/exam/<id>/snapshot/ and stored as ProctorSnapshot.")

h2("Tab Switch Detection  (3 overlapping events)")
table(
    ["Event", "Trigger", "Priority"],
    [
        ("fullscreenchange",      "Student exits fullscreen (most reliable)", "Primary"),
        ("document.visibilitychange", "Browser tab switch",                   "Secondary"),
        ("window blur",           "Alt+Tab / app switch",                     "Tertiary"),
    ]
)

h2("Penalty Logic")
bul("1st & 2nd switch: warning overlay shown, tab_switch_count incremented.")
bul("3rd switch: server auto-submits exam via /api/exam/<id>/tab-switch/ endpoint.")
bul("Additional measures: copy/paste disabled, right-click blocked, fullscreen enforced on load.")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — API ENDPOINTS & ADMIN
# ══════════════════════════════════════════════════════════════════════════════
h1("9.  API Endpoints & Admin Interface")

h2("AJAX / JSON Endpoints")
table(
    ["Method", "URL", "Purpose"],
    [
        ("POST", "/api/exam/<id>/save-answer/<qid>/", "Save/update a single answer"),
        ("POST", "/api/exam/<id>/tab-switch/",        "Record tab switch; auto-submit on 3rd"),
        ("POST", "/api/exam/<id>/submit/",            "Grade all answers and finalize exam"),
        ("GET",  "/api/exam/<id>/time-remaining/",    "Return seconds left as JSON"),
        ("POST", "/api/exam/<id>/snapshot/",          "Store base64 webcam snapshot"),
        ("POST", "/api/code/run/",                    "Compile & run C code; return output"),
    ]
)

h2("Admin Panel  (/admin/)")
bul("StudentProxy / TeacherProxy — manage user accounts by role")
bul("Exam + inline Questions — create and edit exams")
bul("StudentExam — track attempts, marks, tab-switch counts")
bul("ProctorSnapshot — browse/filter webcam evidence")
bul("PasswordResetOTP — audit OTP requests")
body("Create Teacher accounts ONLY via Admin (self-registration is disabled for teachers).")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — DEPLOYMENT
# ══════════════════════════════════════════════════════════════════════════════
h1("10.  Deployment (Production)")

h2("Settings Changes")
bul("DEBUG = False  |  ALLOWED_HOSTS = ['yourdomain.com']")
bul("Generate new SECRET_KEY via django.core.management.utils.get_random_secret_key()")
bul("Switch to PostgreSQL database (psycopg2-binary already in requirements.txt)")
bul("Configure real SMTP for email (EMAIL_BACKEND = 'smtp.EmailBackend')")

h2("Deploy Steps")
num("python manage.py collectstatic --noinput")
num("python manage.py migrate")
num("gunicorn Exam.wsgi:application --bind 0.0.0.0:8000 --workers 3")
num("Configure Nginx to proxy-pass to Gunicorn and serve /static/ from staticfiles/")
num("Install SSL certificate (Let's Encrypt) — required for webcam access in browsers")

# ── Save ──────────────────────────────────────────────────────────────────────
doc.save("Implementation_Steps_v2.docx")
print("Done — Implementation_Steps_v2.docx saved (5 pages).")
