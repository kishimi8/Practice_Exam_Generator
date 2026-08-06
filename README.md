# Microsoft Certification Practice Exam Engine

A terminal-based, data-driven Python exam runner for any Microsoft certification.  
All questions live in plain **JSON files** — the engine (`exam.py`) contains zero exam content.

```
dp600-exam/
├── exam.py              ← engine (never edit this to add questions)
├── courses/
│   ├── dp600.json       ← DP-600: Microsoft Fabric  (50 Qs)
│   ├── pl300.json       ← PL-300: Power BI          (36 Qs)
│   └── <yourexam>.json  ← add any new course here
└── README.md
```

---

## Running the exam

```bash
python3 exam.py
```

The engine auto-discovers every `.json` file in `courses/` and presents a course picker.

---

## How to add questions to an existing course

Open the course JSON file (e.g. `courses/dp600.json`) and append a new object to the
`"questions"` array.  Follow this schema exactly:

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
| `domain` | Must exactly match one of the strings in the top-level `"domains"` array, or it won't group correctly. |
| `text` | The question stem. |
| `options` | Array of `{"key", "text"}` objects. Keys are typically A–E but can be anything. |
| `correct` | Must match exactly one `"key"` value from `options`. |
| `explanation` | Shown immediately after the user answers. Keep it concise but complete. |

> **Tip:** You can have 5 options (A–E) for "select the best" style questions, or just 2 (True/False).  
> The engine adapts automatically — whatever keys you define become the valid input letters.

---

## How to add a brand-new course (new exam)

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

3. Save the file. Next time you run `python3 exam.py`, the new course appears automatically in the picker.

---

## Top-level JSON fields reference

| Field | Type | Description |
|---|---|---|
| `id` | string | Machine-readable identifier (e.g. `"az900"`). Not displayed. |
| `title` | string | Full exam title shown in headers. |
| `short_title` | string | Compact title shown in the course picker. |
| `passing_score` | int | Minimum correct answers to pass. Shown on results screen. |
| `description` | string | One-line description (not yet displayed but useful for documentation). |
| `domains` | array of strings | Domain labels. Each question's `"domain"` must match one of these. |
| `scoring_guide` | array of objects | Verdict bands. Each object has `"min"` (int) and `"label"` (string). Listed from highest to lowest threshold. |
| `questions` | array of objects | The question bank. See schema above. |

---

## Suggested Microsoft courses to add

| Exam | Topic |
|---|---|
| `AZ-900` | Azure Fundamentals |
| `AZ-104` | Azure Administrator |
| `AZ-204` | Developing Solutions for Azure |
| `AZ-305` | Designing Azure Infrastructure |
| `AI-900` | AI Fundamentals |
| `AI-102` | Designing AI Solutions |
| `DP-900` | Data Fundamentals |
| `DP-203` | Data Engineering on Azure |
| `SC-900` | Security Fundamentals |
| `MS-900` | Microsoft 365 Fundamentals |
