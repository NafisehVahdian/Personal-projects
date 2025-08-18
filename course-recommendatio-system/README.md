# CoursePass — High‑Precision Course Recommender (Sharif CS Synthetic Datasets)

**Maintainer:** Nafiseh Vahidian  
**Version:** v1.0 • **Release date:** 2025-08-18  
**Scope:** Undergraduate **BSc in Computer Science** at **Sharif University of Technology (SUT)**  
**Language:** English‑only • **License:** MIT (suggested)

---

## 🚀 Project Overview

**CoursePass** is a research/teaching project to build a **high‑precision course recommender** that only suggests courses a student is **very likely to pass**.  
The system predicts a **probability of passing** for each eligible course and recommends items that meet a strict confidence threshold (e.g., ≥ 0.85), while enforcing **prerequisites** and other academic policies.

This repository ships with **synthetic, privacy‑safe datasets** that mirror a typical CS curriculum at Sharif University. They are ready for:
- Item‑item similarity baselines
- Grade‑aware models (logistic/GBM/wide‑and‑deep)
- Risk‑controlled selection (e.g., conformal prediction)
- Reproducible offline evaluation with temporal splits

> ⚠️ All data in this repo are **synthetic** and generated for education/research demos. No real student records are included.

---

## 📦 Datasets

**Files** (CSV):
- `sut_courses.csv` — Course catalog with prerequisites and core/elective flag.  
- `sut_students.csv` — Synthetic CS undergraduates (40 students, cohorts 2021–2024).  
- `sut_enrollments.csv` — Per‑term enrollments with numeric grades (0–20) and derived letters.

**Download:**  
- Datasets: `sut_datasets.zip` (bundled)  
- Standalone files are also provided alongside this README.

---

## 🧱 Schemas (Data Dictionary)

### `sut_courses.csv`
| column | type | description |
|---|---|---|
| `course_id` | string | Unique ID (e.g., `SUT-40424`) |
| `title` | string | Course title |
| `dept` | string | Department code (CS, EE, ENGR, MATH, PHYS, STAT) |
| `level` | int | 100, 200, 300, 400 (intro → advanced) |
| `credits` | int | Course credit units (0 allowed for internship) |
| `prerequisites` | string | `|`‑separated course IDs; empty if none |
| `is_core` | int (0/1) | 1 for core, 0 for elective |

### `sut_students.csv`
| column | type | description |
|---|---|---|
| `student_id` | string | Primary key (e.g., `SUT1000xxxx`) |
| `name` | string | Synthetic name |
| `university` | string | Always `Sharif University of Technology` |
| `program` | string | `BSc Computer Science` |
| `cohort_year` | int | Entry year (2021–2024) |
| `level` | string | `UG` |
| `gpa_20` | float | GPA on 0–20 scale |
| `completed_credits` | int | Rough synthetic estimate |

### `sut_enrollments.csv`
| column | type | description |
|---|---|---|
| `student_id` | FK | → `sut_students.student_id` |
| `course_id` | FK | → `sut_courses.course_id` |
| `term` | string | `Fall` or `Spring` |
| `year` | int | 2021–2027 |
| `grade_20` | float | 0–20 numeric grade |
| `grade_letter` | string | One of `A+`, `A`, `B`, `C`, `D`, `F` |

**Grading system**
- Primary: **0–20** numeric  
- Letter mapping used here: A+ (18–20), A (17–17.99), B (14–16.99), C (12–13.99), D (10–11.99), F (<10)  
- **Pass threshold:** `grade_20 ≥ 10`

---

## 📊 Quick Stats

**Courses**
- Total: **56** (Core: **28**, Electives: **28**)  
- Departments: CS, EE, ENGR, MATH, PHYS, STAT  
- Levels: 0, 100, 200, 300, 400  
- Avg credits: **2.66**

Top‑10 most‑taken courses:
| course_id   |   times_taken | title                           | dept   |   level |
|:------------|--------------:|:--------------------------------|:-------|--------:|
| SUT-40153   |            40 | Programming Fundamentals        | CS     |     100 |
| SUT-24011   |            40 | Physics I                       | PHYS   |     100 |
| SUT-40212   |            40 | Logic Circuits                  | CS     |     200 |
| SUT-40115   |            40 | Discrete Structures             | CS     |     200 |
| SUT-22015   |            40 | Calculus I                      | MATH   |     100 |
| SUT-40211   |            40 | Technical English for Computing | CS     |     200 |
| SUT-33018   |            40 | General Workshop                | ENGR   |     100 |
| SUT-40108   |            40 | Computer Workshop               | CS     |     100 |
| SUT-40244   |            38 | Advanced Programming            | CS     |     200 |
| SUT-24002   |            38 | Physics II Lab                  | PHYS   |     100 |

**Students**
- Total: **40**  
- Cohorts:  
  - 2021: 14 students
  - 2022: 8 students
  - 2023: 6 students
  - 2024: 12 students  
- Avg GPA (0–20): **15.6**

**Enrollments**
- Rows: **1321**  
- Terms: Fall, Spring • Years: **2021–2027**  
- Overall pass rate (≥10): **94.9%**  
- Letter distribution:  
  - A: 152
  - A+: 182
  - B: 585
  - C: 263
  - D: 71
  - F: 68

---

## 🧪 Recommended Modeling Workflow (High‑Precision “Pass” Recs)

1. **Eligibility filter**: prerequisites satisfied; sensible level progression; exclude already‑taken courses.  
2. **Predict** `P(pass | student, course)` with a calibrated model (e.g., logistic with student/course bias + features).  
3. **Selective policy**: recommend only if `P(pass) ≥ τ` (e.g., 0.85) **and** predicted risk meets a conformal bound (e.g., fail ≤ 5%).  
4. **Explain** each rec with nearest passed courses (item‑item similarity) + student’s historical performance by dept/level.  
5. **Evaluate** with temporal split (train ≤ 2024, test 2025) using: Precision@K, coverage, fail‑rate among recommended, Brier score, calibration curves.

> This section describes the intended project behavior for GitHub readers; code can be added later.

---

## 📁 Suggested Repo Structure

```
.
├─ data/
│  ├─ sut_courses.csv
│  ├─ sut_students.csv
│  └─ sut_enrollments.csv
├─ notebooks/
│  ├─ 01_explore.ipynb
│  ├─ 02_features.ipynb
│  ├─ 03_model.ipynb
│  └─ 04_conformal_selection.ipynb
├─ src/
│  ├─ data_loading.py
│  ├─ features.py
│  ├─ model.py
│  └─ selection.py
├─ README.md
└─ LICENSE
```

---

## 🗃️ ER Diagram (ASCII)

```
sut_students                sut_enrollments                     sut_courses
-------------               ----------------                     -----------
student_id (PK) <-------+   student_id (FK)  -----------+-----> course_id (PK)
name                     \  course_id  (FK)  ----+       \      title
university                \ term                 \        \     dept, level, credits
program                    \ year                  \        \    prerequisites
cohort_year                 \ grade_20              \        \   is_core
level                        \ grade_letter         (composite PK: student_id, course_id, term, year)
gpa_20                        \ 
completed_credits             ```

---

## 🧰 Getting Started

**Python**
```python
import pandas as pd

courses = pd.read_csv("data/sut_courses.csv")
students = pd.read_csv("data/sut_students.csv")
enr = pd.read_csv("data/sut_enrollments.csv")

# pass label
enr["passed"] = (enr["grade_20"] >= 10).astype(int)
```

**SQL (DDL sketch)**
```sql
CREATE TABLE sut_courses (
  course_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  dept TEXT NOT NULL,
  level INT NOT NULL,
  credits INT NOT NULL,
  prerequisites TEXT,
  is_core INT NOT NULL CHECK (is_core IN (0,1))
);

CREATE TABLE sut_students (
  student_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  university TEXT NOT NULL,
  program TEXT NOT NULL,
  cohort_year INT NOT NULL,
  level TEXT NOT NULL,
  gpa_20 REAL NOT NULL,
  completed_credits INT NOT NULL
);

CREATE TABLE sut_enrollments (
  student_id TEXT NOT NULL REFERENCES sut_students(student_id),
  course_id  TEXT NOT NULL REFERENCES sut_courses(course_id),
  term TEXT NOT NULL CHECK (term IN ('Fall','Spring')),
  year INT NOT NULL,
  grade_20 REAL NOT NULL,
  grade_letter TEXT NOT NULL,
  PRIMARY KEY (student_id, course_id, term, year)
);
```

---

## ✅ Ethics & Usage

- Synthetic and privacy‑safe; suitable for classroom demos and public repos.  
- Do **not** use these data to make real academic decisions.  
- If you publish results, clarify that the data are **synthetic**.

---

## 📜 Citation

If you use this repo, please cite:

```
Vahidian, N. (2025). CoursePass: High-Precision Course Recommender (Sharif CS Synthetic Datasets). GitHub repository.
```

---

## 📝 License

Suggested: **MIT License**. Add a `LICENSE` file to your repo root.

---

## 🙌 Acknowledgements

Thanks to open academic course charts and community best practices for educational dataset design. Curriculum structure and grading scale were approximated for realism; any mismatch with official materials is unintentional.
