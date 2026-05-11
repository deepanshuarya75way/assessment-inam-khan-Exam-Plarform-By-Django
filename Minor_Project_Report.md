# MINOR PROJECT REPORT
### Project Term: January – May 2025
## ONLINE EXAMINATION PLATFORM WITH AUTOMATED PROCTORING AND C CODE EVALUATION

**Submitted by:** Inam Khan | Reg. No.: _______________ | Programme & Section: _______________
**Under Guidance of:** _______________ | Dept. of CSE | Lovely Professional University, Phagwara

---

## DECLARATION

I declare that the project **"Online Examination Platform with Automated Proctoring and C Code Evaluation"** is an authentic record of my own work carried out as requirements of Minor Project for the award of _______________ from Lovely Professional University, under the guidance of _______________, during January–May 2025.

(Signature) **Inam Khan** | Reg. No.: _______________ | Date: ___________

Certified that the above statement is correct.  _______________ (Name, U.ID, Designation) | Faculty Mentor

---

## ACKNOWLEDGEMENT

I express my profound gratitude to _______________ (HOD) and _______________ (HOS) of Lovely Professional University for their support. Special thanks to my mentor _______________ for continuous guidance. I acknowledge that this project was completed entirely by me.

**Inam Khan** | Reg. No.: _______________

---

## TABLE OF CONTENTS

| DESCRIPTION | PAGE |
|---|---|
| Declaration | iii |
| Acknowledgements | iv |
| List of Figures | v |
| List of Tables | vi |
| 1. Profile of the Problem (Introduction) | 1 |
| 2. Existing System | 3 |
| 3. Problem Analysis | 5 |
| 4. Software Requirement Analysis | 6 |
| 5. Design | 9 |
| 6. Implementation | 14 |
| 7. Bibliography | 22 |

---

## LIST OF FIGURES

| FIGURE | TITLE | PAGE |
|---|---|---|
| 5.1 | DFD Level 0 – Context Diagram | 9 |
| 5.2 | DFD Level 1 – Main Processes | 10 |
| 5.3 | ER Diagram | 11 |
| 6.1 | Home Page | 20 |
| 6.2 | Student Dashboard | 20 |
| 6.3 | Exam Interface | 21 |
| 6.4 | Teacher Dashboard | 21 |
| 6.5 | Proctoring Snapshots View | 22 |

## LIST OF TABLES

| TABLE | TITLE | PAGE |
|---|---|---|
| 2.1 | Comparison of Existing Platforms | 3 |
| 4.1 | Functional & Non-Functional Requirements | 6 |
| 4.2 | Tools and Technologies | 8 |
| 5.1 | Database Table Designs | 11 |

---

# CHAPTER 1: PROFILE OF THE PROBLEM (INTRODUCTION)

## 1.1 Introduction

Online education has made digital examination systems a necessity, especially for programming-based courses. Existing free tools like Google Forms lack code execution support, while commercial platforms like HackerRank are expensive and store student data on external servers.

This project — **"Online Examination Platform with Automated Proctoring and C Code Evaluation"** — is a self-hosted Django web application that allows teachers to create multi-type exams (MCQ, True/False, Short Answer, C Coding), auto-grades C submissions using a local GCC compiler, and monitors students through webcam/screen proctoring and tab-switch detection.

## 1.2 Objectives

1. Build a dual-role (Teacher/Student) Django web application.
2. Support four question types: MCQ, True/False, Short Answer, and C Coding.
3. Auto-grade C code by compiling and running against test cases using local GCC.
4. Implement real-time proctoring via webcam and screen capture.
5. Detect tab-switching and auto-submit after 3 violations.
6. Provide secure OTP-based password reset.
7. Use only free, open-source technologies — no external API dependency.

---

# CHAPTER 2: EXISTING SYSTEM

## 2.1 Existing Software

**Table 2.1 – Comparison of Existing Exam Platforms**

| Feature | Google Forms | Moodle | HackerRank | Our System |
|---|---|---|---|---|
| MCQ Support | Yes | Yes | Yes | Yes |
| C Code Evaluation | No | Via Plugin | Yes | Yes |
| Built-in Proctoring | No | No | Yes (paid) | Yes |
| Tab-Switch Detection | No | No | Yes | Yes |
| Self-Hosted / Free | Yes | Yes | No | Yes |
| OTP Password Reset | No | No | No | Yes |

## 2.2 Drawbacks of Existing Systems

- Google Forms and standard LMS tools do not support live code execution.
- HackerRank and Codility are subscription-based; student data stored on external servers.
- Moodle requires complex VPL plugin setup for coding support.
- Dedicated proctoring services (ProctorU) transmit biometric data to third-party servers.

## 2.3 What's New in the Proposed System

- **Local GCC integration:** C code compiled and run server-side with no external API.
- **Mixed question types:** MCQ + Coding in a single exam.
- **Hidden test cases:** Students cannot reverse-engineer grading criteria.
- **Data sovereignty:** All snapshots and exam data stored locally.
- **Auto-submit on 3 tab switches** enforced server-side.

---

# CHAPTER 3: PROBLEM ANALYSIS

## 3.1 Problem Definition

Design and implement a web-based examination platform that enables teachers to create mixed-type exams, automatically grades C code locally, monitors student behaviour through proctoring, and provides post-exam review — entirely self-hosted and open-source.

## 3.2 Project Plan

| Phase | Activity | Weeks |
|---|---|---|
| 1 | Requirement Analysis | 1–2 |
| 2 | System Design (ER, DFD) | 3–4 |
| 3 | Database Models & Migrations | 5–6 |
| 4 | Auth Module (Login, OTP) | 6–7 |
| 5 | Teacher Module | 7–9 |
| 6 | Student & Exam Module | 9–11 |
| 7 | C Code Execution Engine | 10–12 |
| 8 | Proctoring Module | 12–13 |
| 9 | Testing & Bug Fix | 13–15 |
| 10 | Documentation | 15–16 |

---

# CHAPTER 4: SOFTWARE REQUIREMENT ANALYSIS

## 4.1 General Description

Django MVT-based web application with a single app (`Examapp`) containing all models, views, and templates. SQLite used for development; PostgreSQL supported for production. Static files served via WhiteNoise middleware.

## 4.2 Functional Requirements

**Table 4.1 – Functional Requirements**

| FR No. | Requirement |
|---|---|
| FR-01 | Students self-register using name, reg. number, email, course, section, password. |
| FR-02 | Teacher accounts created only by Django admin. |
| FR-03 | Login requires role selection and credential verification. |
| FR-04 | Password reset via 6-digit OTP (valid 10 minutes). |
| FR-05 | Teachers create exams with title, duration, start/end time, total/passing marks. |
| FR-06 | Teachers add four question types: MCQ, True/False, Short Answer, Coding (C). |
| FR-07 | Coding questions support test cases with stdin, expected output, marks, hidden flag. |
| FR-08 | Teachers assign students to exams and publish them. |
| FR-09 | Students view exams as: Upcoming / Available / Completed. |
| FR-10 | Exam interface shows countdown timer; answers auto-saved via AJAX. |
| FR-11 | C code compiled and executed locally; matched against all test cases. |
| FR-12 | Webcam and screen snapshots captured every 30 seconds. |
| FR-13 | On 3rd tab-switch, exam auto-submitted server-side. |
| FR-14 | Teachers review student answers and proctoring snapshots post-exam. |

## 4.3 Non-Functional Requirements

| NFR | Category | Requirement |
|---|---|---|
| NFR-01 | Security | Passwords: PBKDF2-SHA256 hashes. CSRF protection on all forms. |
| NFR-02 | Security | C code runs in isolated temp dir deleted after execution. |
| NFR-03 | Performance | Compile timeout: 15 sec. Run timeout: 5 sec. Memory: 64 MB. |
| NFR-04 | Reliability | Auto-save prevents answer loss on navigation. |
| NFR-05 | Data Integrity | Submitted exam cannot be resubmitted (server-side guard). |

## 4.4 Tools and Technologies

**Table 4.3 – Tools and Technologies**

| Category | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ |
| Web Framework | Django | 6.0.3 |
| Database (Dev/Prod) | SQLite / PostgreSQL | 3.x / 15+ |
| Static Files | WhiteNoise | 6.12.0 |
| WSGI Server | Gunicorn | 25.3.0 |
| C Compiler | GCC / Clang | System |
| Frontend | HTML5, CSS3, JavaScript | – |
| Browser API | MediaDevices API (Webcam) | – |

---

# CHAPTER 5: DESIGN

## 5.1 DFD

**Figure 5.1 – DFD Level 0 (Context Diagram)**

```
STUDENT ──► [ ONLINE EXAM PLATFORM ] ──► STUDENT (Results, Questions)
TEACHER ──►                           ──► TEACHER (Results, Snapshots)
```

**Figure 5.2 – DFD Level 1**

```
 ┌─────────────┐   ┌────────────────────┐   ┌──────────────────────┐
 │ 1.0 AUTH    │   │ 2.0 EXAM MGMT      │   │ 3.0 EXAM ATTEMPT     │
 │ Register    │   │ Create/Edit Exam   │   │ Start / Answer / Save│
 │ Login / OTP │   │ Add Questions      │   │ Timer / Submit       │
 └─────────────┘   │ Assign Students    │   └──────────┬───────────┘
                   └────────┬───────────┘              │
                            └──────────────┬───────────┘
                                    ┌──────▼──────────────────────┐
                                    │ 4.0 GRADING ENGINE          │
                                    │ MCQ/TF→Auto | C→GCC runner  │
                                    └──────┬──────────────────────┘
                                    ┌──────▼──────────────────────┐
                                    │ 5.0 PROCTORING              │
                                    │ Webcam + Screen + TabSwitch │
                                    └─────────────────────────────┘
```

## 5.2 ER Diagram

**Figure 5.3 – ER Diagram**

```
 User ──1:1── UserRole
 User ──1:N── Exam (as teacher)
 User ──1:N── PasswordResetOTP
 Exam ──1:N── Question ──1:N── Choice
                        ──1:N── CodingTestCase
 Exam ──1:N── StudentExam ──1:N── Answer
                           ──1:N── ProctorSnapshot
```

## 5.3 Table Design

**Table 5.1 – Database Table Designs**

**Exam**

| Column | Type | Description |
|---|---|---|
| teacher_id | FK → User | Creator |
| title | VARCHAR(200) | Exam title |
| duration_minutes | Integer | Time limit |
| start_time / end_time | DateTime | Active window |
| total_marks / passing_marks | Integer | Marks config |
| is_published | Boolean | Visible to students |

**Question**

| Column | Type | Description |
|---|---|---|
| exam_id | FK → Exam | Parent exam |
| question_type | VARCHAR(20) | mcq / true_false / short_answer / coding |
| marks | Integer | Marks for this question |
| order | Integer | Display sequence |

**CodingTestCase**

| Column | Type | Description |
|---|---|---|
| question_id | FK → Question | Parent coding question |
| stdin | TextField | Standard input |
| expected_output | TextField | Expected stdout |
| marks | Integer | Marks if passed |
| is_hidden | Boolean | Hidden from student |

**StudentExam**

| Column | Type | Description |
|---|---|---|
| student_id / exam_id | FK | Student-Exam link |
| is_submitted | Boolean | Submission status |
| obtained_marks | Integer (null) | Final marks |
| tab_switch_count | Integer | Violations |

**Answer**

| Column | Type | Description |
|---|---|---|
| student_exam_id / question_id | FK | Links answer to session |
| selected_choice_id | FK (null) | For MCQ/TF |
| written_answer | TextField | For Short/Coding |
| marks_obtained | Integer (null) | Awarded marks |

**ProctorSnapshot**

| Column | Type | Description |
|---|---|---|
| student_exam_id | FK | Exam session |
| snapshot_type | VARCHAR(10) | webcam / screen |
| image_data | TextField | Base64-encoded JPEG |
| is_flagged | Boolean | Flagged for review |

---

# CHAPTER 6: IMPLEMENTATION

## 6.1 Code Modules

### Module 1 – C Code Execution Engine

```python
def _execute_c_code(code, stdin):
    compiler   = getattr(django_settings, 'LOCAL_C_COMPILER', '/usr/bin/gcc')
    time_limit = getattr(django_settings, 'LOCAL_C_TIME_LIMIT', 5)
    work_dir = tempfile.mkdtemp(prefix='exam_c_')
    src_path = os.path.join(work_dir, 'solution.c')
    bin_path = os.path.join(work_dir, 'solution')
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
        shutil.rmtree(work_dir, ignore_errors=True)
```

### Module 2 – Tab-Switch Detection & Auto-Submit

```python
@require_POST
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
                    answer.marks_obtained = q.marks
                    total += q.marks
                else:
                    answer.marks_obtained = 0
            elif q.question_type == 'coding':
                m, graded = _grade_coding_answer(q, answer.written_answer or '')
                if graded and m is not None:
                    answer.marks_obtained = m
                    total += m
            answer.save()
        student_exam.obtained_marks = total
        student_exam.is_submitted = True
        student_exam.submitted_at = timezone.now()
        student_exam.save()
        return JsonResponse({'status': 'auto_submit',
                             'redirect_url': reverse('exam_result', args=[student_exam.id])})
    return JsonResponse({'status': 'recorded', 'tab_switch_count': student_exam.tab_switch_count})
```

### Module 3 – OTP Password Reset

```python
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'auth/forgot_password.html',
                          {'error': 'No account found with this email.'})
        otp = f"{random.randint(100000, 999999)}"
        PasswordResetOTP.objects.create(user=user, otp=otp)
        send_mail(subject='Password Reset OTP',
                  message=f'Your OTP: {otp}  (valid 10 min)',
                  from_email=None, recipient_list=[email])
        request.session['reset_user_id'] = user.id
        return redirect('verify_otp')
    return render(request, 'auth/forgot_password.html')
```

### Module 4 – Proctoring Snapshot API

```python
@require_POST
@login_required(login_url='login')
def save_snapshot(request, student_exam_id):
    student_exam = get_object_or_404(StudentExam, id=student_exam_id, student=request.user)
    data        = json.loads(request.body)
    image_b64   = data.get('image', '').strip()
    snap_type   = data.get('type', 'webcam')
    flag_reason = data.get('flag_reason', '')
    if not image_b64 or len(image_b64) < 100:
        return JsonResponse({'status': 'error'}, status=400)
    ProctorSnapshot.objects.create(
        student_exam=student_exam, snapshot_type=snap_type,
        image_data=image_b64, is_flagged=bool(flag_reason), flag_reason=flag_reason,
    )
    return JsonResponse({'status': 'saved'})
```

## 6.2 Screenshots of the Project

**Figure 6.1 – Home Page**
*(Insert screenshot here)*

**Figure 6.2 – Student Dashboard (Upcoming / Available / Completed exams)**
*(Insert screenshot here)*

**Figure 6.3 – Exam Interface (Questions + timer + code editor)**
*(Insert screenshot here)*

**Figure 6.4 – Teacher Dashboard (Exam list)**
*(Insert screenshot here)*

**Figure 6.5 – Proctoring Snapshots (Flagged images for review)**
*(Insert screenshot here)*

---

# CHAPTER 7: BIBLIOGRAPHY

1. Django Software Foundation. (2024). *Django Documentation v6.0*. https://docs.djangoproject.com/
2. Python Software Foundation. (2024). *Python 3 Documentation*. https://docs.python.org/3/
3. WhiteNoise. (2024). *Static file serving for Python*. https://whitenoise.readthedocs.io/
4. Free Software Foundation. (2024). *GCC, the GNU Compiler Collection*. https://gcc.gnu.org/
5. Mozilla Developer Network. (2024). *MediaDevices.getUserMedia() API*. https://developer.mozilla.org/
6. Sommerville, I. (2015). *Software Engineering* (10th ed.). Pearson Education.
7. Pressman, R. S. & Maxim, B. R. (2019). *Software Engineering: A Practitioner's Approach* (9th ed.). McGraw-Hill.

---
*Inam Khan | Lovely Professional University | January – May 2025*
