# Practice Exam Engine

A Python-based certification exam practice suite with both a CLI engine and a modern GUI client. All exam content is stored in plain **JSON files** so the app remains content-agnostic.

```
Practice_Exam_Generator/
├── exam.py              ← CLI practice exam engine
├── exam_gui.py          ← Qt-based GUI front end
├── courses/
│   ├── dp600.json       ← DP-600: Microsoft Fabric  (50 Qs)
│   ├── pl300.json       ← PL-300: Power BI          (36 Qs)
│   └── <yourexam>.json  ← add any new course here
├── saves/               ← saved GUI sessions (created automatically)
└── README.md
```

---

## Overview

The GUI supports the same course and question format as the CLI `exam.py`, with added features for:
- exam hub dashboard and performance analytics
- saved session resume/reload
- import practice exams as JSON files
- multiple exam modes: full, shuffled, quick drill, domain focus
- answer feedback, explanations, and review screens
- domain-level performance breakdowns

The GUI is implemented in `exam_gui.py` and auto-discovers every `.json` file in `courses/`.

---

## Requirements

The GUI runs with one of these Qt bindings:
- `PySide6` (recommended)
- `PyQt6`
- `PyQt5`

Install the recommended dependency with:

```bash
python3 -m pip install PySide6
```

---

## Running the GUI

```bash
python3 exam_gui.py
```

If no supported Qt binding is installed, the app will exit with an instruction to install `PySide6`.

---

## Running the CLI

The CLI runner still works as before:

```bash
python3 exam.py
```

The CLI and GUI share the same course JSON format, but the GUI adds a richer visual experience and saved-session workflow.

---

## GUI Features

### Main Hub
- dashboard metrics for total exams attempted, pass rate, and average score
- strongest domains breakdown from prior completed sessions
- buttons to start a new exam, resume a saved session, import a practice exam, reset stats, or exit

### Course selection
- pick from all `.json` files found in `courses/`
- shows each course's short title and question count

### Exam mode selection
- `Full Exam - Normal Order`
- `Full Exam - Shuffled Order`
- `Quick Drill - Custom Number of Questions`
- `Domain Focus - Target Specific Knowledge Objectives`

### Exam screen
- timed session timer
- progress bar showing current question and total questions
- answers displayed as clickable option cards
- question flagging for later review
- `Skip Question` to move to the next unanswered item
- `Save & Exit Session` to persist progress into `saves/`
- instant answer evaluation and explanation feedback

### Results analysis
- score and verdict with styled pass/fail coloring
- passing threshold display
- domain-by-domain performance progress bars
- review incorrect answers or review every question after completion

### Saved sessions
- all saved GUI sessions live under `saves/`
- saved sessions store the exam state, elapsed time, answered questions, and flags
- resume a saved session from the GUI resume screen
- delete old saved sessions from the GUI

### Performance history
- completion history is recorded in `history.json`
- the hub aggregates pass rate, average score, and domain strengths from completed exams

---

## How to add questions to an existing course

Open the course JSON file (e.g. `courses/dp600.json`) and append a new object to the `questions` array. Follow this schema exactly:

```json
{
  "number": 51,
  "domain": "Domain 2 · Prepare and Serve Data",
  "text": "Your question text goes here.",
  "options": [
    { "key": "A", "text": "First option" },
    { "key": "B", "text": "Second option" },
    { "key": "C", "text": "Third option" },
    { "key": "D", "text": "Fourth option" }
  ],
  "correct": "B",
  "explanation": "Why B is correct — shown to the user after they answer."
}
```

### Rules
| Field | Requirement |
|---|---|
| `number` | Any integer. Used only for display. Does not need to be sequential or unique across courses. |
| `domain` | Must exactly match one of the strings in the top-level `domains` array, or it won't group correctly. |
| `text` | The question stem. |
| `options` | Array of objects with `key` and `text`. Keys are typically A–E but can be anything. |
| `correct` | Must match exactly one `key` value from `options`. |
| `explanation` | Shown immediately after the user answers. Keep it concise but complete. |

> **Tip:** You can have 5 options (A–E) for "select the best" style questions, or just 2 (True/False). The app adapts automatically to the keys you define.

---

## How to add a brand-new course

1. Create a new file: `courses/<exam-id>.json`
2. Use the template below:

```json
{
  "id": "az900",
  "title": "AZ-900: Microsoft Azure Fundamentals",
  "short_title": "AZ-900 · Azure Fundamentals",
  "passing_score": 42,
  "description": "Covers core Azure concepts, services, pricing, and support.",
  "domains": [
    "Domain 1 · Cloud Concepts",
    "Domain 2 · Azure Architecture & Services",
    "Domain 3 · Azure Management & Governance"
  ],
  "scoring_guide": [
    { "min": 42, "label": "EXCELLENT — Likely exam-ready!" },
    { "min": 35, "label": "GOOD — Review missed domains." },
    { "min": 0,  "label": "NEEDS WORK — Study the weak domains." }
  ],
  "questions": [
    {
      "number": 1,
      "domain": "Domain 1 · Cloud Concepts",
      "text": "Which cloud deployment model provides resources exclusively to one organization?",
      "options": [
        { "key": "A", "text": "Public cloud" },
        { "key": "B", "text": "Private cloud" },
        { "key": "C", "text": "Hybrid cloud" },
        { "key": "D", "text": "Community cloud" }
      ],
      "correct": "B",
      "explanation": "A private cloud is dedicated to a single organization and can be hosted on-premises or by a third-party provider."
    }
  ]
}
```

3. Save the file. Next time you run `python3 exam_gui.py` or `python3 exam.py`, the new course appears automatically in the picker.

---

## Top-level JSON fields reference

| Field | Type | Description |
|---|---|---|
| `id` | string | Machine-readable identifier (e.g. `"az900"`). Not displayed. |
| `title` | string | Full exam title shown in headers. |
| `short_title` | string | Compact title shown in the course picker. |
| `passing_score` | int | Minimum correct answers to pass. Shown on results screen. |
| `description` | string | One-line description for the course file. |
| `domains` | array of strings | Domain labels. Each question's `domain` must match one of these. |
| `scoring_guide` | array of objects | Verdict bands. Each object has `min` and `label`. Listed from highest to lowest threshold. |
| `questions` | array of objects | The question bank. See schema above. |

---

## Suggested Microsoft courses to add

| Exam | Topic |
|---|---|
| `AZ-900` | Azure Fundamentals |
| `AZ-104` | Azure Administrator |
| `AZ-204` | Developing Solutions for Azure |
| `AZ-305` | Designing Azure Architecture |
| `AI-900` | AI Fundamentals |
| `AI-102` | Designing AI Solutions |
| `DP-900` | Data Fundamentals |
| `DP-203` | Data Engineering on Azure |
| `SC-900` | Security Fundamentals |
| `MS-900` | Microsoft 365 Fundamentals |
