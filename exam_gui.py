#!/usr/bin/env python3
"""
Microsoft Certification Practice Exam — Qt GUI Application
──────────────────────────────────────────────────────────
A premium GUI client using PySide6 (or PyQt6/PyQt5 fallback).
Maintains identical directory structures and database formats as the CLI engine:
- Shared course JSONs in courses/
- Shared save states in saves/
- Shared performance history in history.json
"""

import sys
import os
import json
import random
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# Setup directories
SCRIPT_DIR = Path(__file__).parent.resolve()
COURSES_DIR = SCRIPT_DIR / "courses"
SAVES_DIR = SCRIPT_DIR / "saves"
HISTORY_FILE = SCRIPT_DIR / "history.json"

COURSES_DIR.mkdir(exist_ok=True)
SAVES_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
#  Qt Binding Fallback Wrapper
# ─────────────────────────────────────────────
try:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QStackedWidget, QListWidget, QListWidgetItem,
        QFileDialog, QMessageBox, QRadioButton, QButtonGroup, QScrollArea,
        QProgressBar, QGroupBox, QComboBox, QSpinBox, QFrame
    )
    from PySide6.QtGui import QFont, QColor, QPalette, QIcon
    QT_BINDING = "PySide6"
except ImportError:
    try:
        from PyQt6.QtCore import Qt, QTimer
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QStackedWidget, QListWidget, QListWidgetItem,
            QFileDialog, QMessageBox, QRadioButton, QButtonGroup, QScrollArea,
            QProgressBar, QGroupBox, QComboBox, QSpinBox, QFrame
        )
        from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
        QT_BINDING = "PyQt6"
    except ImportError:
        try:
            from PyQt5.QtCore import Qt, QTimer
            from PyQt5.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QLabel, QPushButton, QStackedWidget, QListWidget, QListWidgetItem,
                QFileDialog, QMessageBox, QRadioButton, QButtonGroup, QScrollArea,
                QProgressBar, QGroupBox, QComboBox, QSpinBox, QFrame
            )
            from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
            QT_BINDING = "PyQt5"
        except ImportError:
            print("Error: PySide6, PyQt6, or PyQt5 must be installed to run the GUI version.")
            print("Please run: pip install PySide6")
            sys.exit(1)

# ─────────────────────────────────────────────
#  Styles / Stylesheet (Modern Slate Dark theme)
# ─────────────────────────────────────────────
QSS_THEME = """
QMainWindow {
    background-color: #0b0f19;
}
QWidget {
    background-color: #0b0f19;
    color: #f1f5f9;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    font-size: 13px;
}
QLabel {
    background: transparent;
}
QFrame#card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    border: none;
    background-color: #0f172a;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background-color: #475569;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background-color: #64748b;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

/* PushButtons styling */
QPushButton {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #e2e8f0;
    padding: 10px 20px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #334155;
    border-color: #0284c7;
}
QPushButton:pressed {
    background-color: #0f172a;
}
QPushButton:disabled {
    background-color: #0f172a;
    border-color: #1e293b;
    color: #64748b;
}

/* Primary buttons */
QPushButton#primaryBtn {
    background-color: #0284c7;
    border: none;
    color: #ffffff;
}
QPushButton#primaryBtn:hover {
    background-color: #0369a1;
}
QPushButton#primaryBtn:pressed {
    background-color: #075985;
}

/* Critical action buttons */
QPushButton#dangerBtn {
    background-color: #7f1d1d;
    border: 1px solid #991b1b;
    color: #fca5a5;
}
QPushButton#dangerBtn:hover {
    background-color: #991b1b;
}

/* Header Text styling */
QLabel#headerTitle {
    font-size: 26px;
    font-weight: 800;
    color: #38bdf8;
}
QLabel#headerSubtitle {
    font-size: 14px;
    color: #94a3b8;
}
QLabel#sectionTitle {
    font-size: 18px;
    font-weight: bold;
    color: #f1f5f9;
    border-bottom: 2px solid #1e293b;
    padding-bottom: 6px;
}

/* List Widgets */
QListWidget {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 5px;
}
QListWidget::item {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 12px;
    margin: 4px;
    color: #f1f5f9;
}
QListWidget::item:hover {
    background-color: #334155;
    border-color: #38bdf8;
}
QListWidget::item:selected {
    background-color: #0284c7;
    border-color: #38bdf8;
    color: #ffffff;
}

/* Option selection layout in exam screen */
QFrame#optionFrame {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #1e293b;
}
QFrame#optionFrame:hover {
    border-color: #38bdf8;
}
QFrame#optionFrame[state="selected"] {
    border: 2px solid #38bdf8;
    background-color: #0f172a;
}
QFrame#optionFrame[state="correct"] {
    border: 2px solid #22c55e;
    background-color: #052e16;
}
QFrame#optionFrame[state="incorrect"] {
    border: 2px solid #ef4444;
    background-color: #450a0a;
}

/* ProgressBar styling */
QProgressBar {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
}
QProgressBar::chunk {
    background-color: #0284c7;
    border-radius: 4px;
}

/* ComboBox / SpinBox */
QComboBox, QSpinBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
    color: #f1f5f9;
}
QComboBox::drop-down {
    border: none;
}
"""

# ─────────────────────────────────────────────
#  Core Data Engine (Same structure as CLI)
# ─────────────────────────────────────────────
@dataclass
class Question:
    number: int
    domain: str
    text: str
    options: list
    correct: str
    explanation: str

    user_answer: Optional[str] = None
    flagged: bool = False
    time_spent: float = 0.0

    @property
    def option_keys(self) -> list[str]:
        return [o["key"] for o in self.options]

    def option_text(self, key: str) -> str:
        for o in self.options:
            if o["key"] == key:
                return o["text"]
        return "—"


@dataclass
class Course:
    id: str
    title: str
    short_title: str
    passing_score: int
    description: str
    domains: list[str]
    scoring_guide: list[dict]
    questions: list[Question]

    def verdict(self, score: int) -> str:
        for tier in sorted(self.scoring_guide, key=lambda t: t["min"], reverse=True):
            if score >= tier["min"]:
                return tier["label"]
        return self.scoring_guide[-1]["label"]

    def verdict_color(self, score: int) -> str:
        n = len(self.questions)
        pct = score / n * 100 if n else 0
        if pct >= 90:  return "#22c55e"
        if pct >= 75:  return "#eab308"
        return "#ef4444"


def load_course(path: Path) -> Course:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    questions = []
    for q in data["questions"]:
        questions.append(Question(
            number=q["number"],
            domain=q["domain"],
            text=q["text"],
            options=q["options"],
            correct=q["correct"],
            explanation=q["explanation"],
        ))
    return Course(
        id=data["id"],
        title=data["title"],
        short_title=data.get("short_title", data["title"]),
        passing_score=data.get("passing_score", 0),
        description=data.get("description", ""),
        domains=data.get("domains", []),
        scoring_guide=data.get("scoring_guide", [{"min": 0, "label": "Complete."}]),
        questions=questions,
    )


def discover_courses() -> List[Dict[str, Any]]:
    if not COURSES_DIR.exists():
        return []
    courses = []
    for p in sorted(COURSES_DIR.glob("*.json")):
        try:
            with open(p, encoding="utf-8") as f:
                meta = json.load(f)
            meta["_path"] = p
            courses.append(meta)
        except Exception:
            pass
    return courses


def load_history() -> List[Dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("history", [])
    except Exception:
        return []


def save_history(history: List[Dict[str, Any]]):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": history}, f, indent=2)
    except Exception:
        pass


def load_exam_states() -> List[Dict[str, Any]]:
    states = []
    for p in SAVES_DIR.glob("*.json"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["_filename"] = p.stem
                states.append(data)
        except Exception:
            pass
    return sorted(states, key=lambda s: s.get("timestamp", ""), reverse=True)


# ─────────────────────────────────────────────
#  Custom Clickable Frame (Option Card Widget)
# ─────────────────────────────────────────────
class OptionCard(QFrame):
    def __init__(self, key: str, text: str, parent=None):
        super().__init__(parent)
        self.setObjectName("optionFrame")
        self.key = key
        self.text = text
        self.clicked_callback = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)

        self.key_lbl = QLabel(f"<b>{key}</b>")
        self.key_lbl.setStyleSheet("color: #38bdf8; font-size: 15px;")
        self.key_lbl.setFixedWidth(25)

        self.text_lbl = QLabel(text)
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setStyleSheet("font-size: 13px;")

        layout.addWidget(self.key_lbl)
        layout.addWidget(self.text_lbl)

    def mousePressEvent(self, event):
        if self.clicked_callback:
            self.clicked_callback(self.key)
        super().mousePressEvent(event)

    def set_state(self, state: str):
        # state can be: "default", "selected", "correct", "incorrect"
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)


# ─────────────────────────────────────────────
#  Application Window
# ─────────────────────────────────────────────
class ExamApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microsoft Certification Exam Suite")
        self.resize(950, 700)
        self.setStyleSheet(QSS_THEME)

        self.current_course: Optional[Course] = None
        self.questions_list: List[Question] = []
        self.current_q_idx = 0
        self.elapsed_timer = 0
        self.timer_obj = QTimer()
        self.timer_obj.timeout.connect(self.update_timer)

        self.loaded_save_name: Optional[str] = None
        self.question_start_time = 0.0

        # Build UI Structure
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)

        self.build_hub_screen()
        self.build_course_select_screen()
        self.build_mode_select_screen()
        self.build_exam_screen()
        self.build_results_screen()
        self.build_resume_screen()

        self.show_hub()

    # ─────────────────────────────────────────────
    #  Screen Builders
    # ─────────────────────────────────────────────
    def build_hub_screen(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Left panel: Stats & Analytics Dashboard
        left_layout = QVBoxLayout()
        lbl_head = QLabel("Exam Hub Dashboard")
        lbl_head.setObjectName("headerTitle")
        lbl_sub = QLabel("Track performance & analytics")
        lbl_sub.setObjectName("headerSubtitle")
        left_layout.addWidget(lbl_head)
        left_layout.addWidget(lbl_sub)
        left_layout.addSpacing(20)

        # Stats Card
        stats_frame = QFrame()
        stats_frame.setObjectName("card")
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_total_taken = QLabel("Total Exams Attempted: 0")
        self.lbl_total_taken.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.lbl_pass_rate = QLabel("Average Pass Rate: 0.0%")
        self.lbl_pass_rate.setStyleSheet("font-size: 14px; font-weight: bold; color: #22c55e;")
        self.lbl_avg_score = QLabel("Average Exam Score: 0.0%")
        self.lbl_avg_score.setStyleSheet("font-size: 14px; font-weight: bold; color: #38bdf8;")

        stats_layout.addWidget(self.lbl_total_taken)
        stats_layout.addWidget(self.lbl_pass_rate)
        stats_layout.addWidget(self.lbl_avg_score)
        left_layout.addWidget(stats_frame)

        # Domain breakdown log area
        left_layout.addSpacing(15)
        lbl_dom_title = QLabel("Strongest Domains")
        lbl_dom_title.setObjectName("sectionTitle")
        left_layout.addWidget(lbl_dom_title)

        self.domains_scroll = QScrollArea()
        self.domains_scroll_content = QWidget()
        self.domains_scroll_layout = QVBoxLayout(self.domains_scroll_content)
        self.domains_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.domains_scroll.setWidget(self.domains_scroll_content)
        self.domains_scroll.setWidgetResizable(True)
        left_layout.addWidget(self.domains_scroll)

        layout.addLayout(left_layout, stretch=2)

        # Right panel: Menu Controls
        right_layout = QVBoxLayout()
        right_layout.addStretch()

        btn_new = QPushButton("Start a New Exam")
        btn_new.setObjectName("primaryBtn")
        btn_new.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn_new.setMinimumHeight(45)
        btn_new.clicked.connect(self.show_course_select)

        btn_resume = QPushButton("Resume a Saved Session")
        btn_resume.setMinimumHeight(45)
        btn_resume.clicked.connect(self.show_resume_picker)

        btn_import = QPushButton("Import Practice Exam (JSON)")
        btn_import.setMinimumHeight(45)
        btn_import.clicked.connect(self.import_course_dialog)

        btn_clear = QPushButton("Reset Performance Stats")
        btn_clear.clicked.connect(self.clear_performance_data)

        btn_quit = QPushButton("Exit Suite")
        btn_quit.setMinimumHeight(45)
        btn_quit.clicked.connect(self.close)

        right_layout.addWidget(btn_new)
        right_layout.addSpacing(12)
        right_layout.addWidget(btn_resume)
        right_layout.addSpacing(12)
        right_layout.addWidget(btn_import)
        right_layout.addSpacing(25)
        right_layout.addWidget(btn_clear)
        right_layout.addSpacing(12)
        right_layout.addWidget(btn_quit)
        right_layout.addStretch()

        layout.addLayout(right_layout, stretch=1)

        self.central_stack.addWidget(widget)

    def build_course_select_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)

        lbl = QLabel("Select a Practice Exam")
        lbl.setObjectName("headerTitle")
        layout.addWidget(lbl)
        layout.addSpacing(20)

        self.course_list = QListWidget()
        layout.addWidget(self.course_list)
        layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back to Hub")
        btn_back.clicked.connect(self.show_hub)
        btn_next = QPushButton("Next (Configure Mode)")
        btn_next.setObjectName("primaryBtn")
        btn_next.clicked.connect(self.go_to_mode_select)

        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_next)
        layout.addLayout(btn_layout)

        self.central_stack.addWidget(widget)

    def build_mode_select_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)

        self.lbl_mode_title = QLabel("Select Exam Mode")
        self.lbl_mode_title.setObjectName("headerTitle")
        layout.addWidget(self.lbl_mode_title)
        layout.addSpacing(20)

        # Mode Options
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Full Exam - Normal Order")
        self.combo_mode.addItem("Full Exam - Shuffled Order")
        self.combo_mode.addItem("Quick Drill - Custom Number of Questions")
        self.combo_mode.addItem("Domain Focus - Target Specific Knowledge Objectives")
        self.combo_mode.currentIndexChanged.connect(self.on_mode_changed)
        layout.addWidget(QLabel("Choose Mode:"))
        layout.addWidget(self.combo_mode)
        layout.addSpacing(15)

        # Frame for conditional input fields
        self.mode_options_frame = QFrame()
        self.mode_options_layout = QVBoxLayout(self.mode_options_frame)
        self.mode_options_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mode_options_frame)
        layout.addSpacing(20)

        # Quick drill widget
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 100)
        self.spin_count.setValue(10)
        self.spin_count_lbl = QLabel("Number of questions:")

        # Domain focus widget
        self.combo_domain = QComboBox()
        self.combo_domain_lbl = QLabel("Select Target Objective:")

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(self.show_course_select)
        btn_start = QPushButton("Start Exam Session")
        btn_start.setObjectName("primaryBtn")
        btn_start.clicked.connect(self.start_new_exam)

        btn_layout.addWidget(btn_back)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_start)
        layout.addLayout(btn_layout)

        self.central_stack.addWidget(widget)

    def build_exam_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 20, 30, 20)

        # Header Info Bar
        info_layout = QHBoxLayout()
        self.lbl_exam_title = QLabel("Exam Title")
        self.lbl_exam_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #38bdf8;")

        self.lbl_timer = QLabel("00:00:00")
        self.lbl_timer.setStyleSheet("font-size: 14px; font-weight: bold; color: #e2e8f0;")

        self.btn_flag = QPushButton("Flag")
        self.btn_flag.setCheckable(True)
        self.btn_flag.setStyleSheet("""
            QPushButton { background-color: #1e293b; color: #e2e8f0; }
            QPushButton:checked { background-color: #854d0e; border-color: #eab308; color: #fef08a; }
        """)
        self.btn_flag.clicked.connect(self.toggle_flag)

        info_layout.addWidget(self.lbl_exam_title)
        info_layout.addStretch()
        info_layout.addWidget(self.lbl_timer)
        info_layout.addWidget(self.btn_flag)
        layout.addLayout(info_layout)

        # Progress indicator bar
        self.exam_progress = QProgressBar()
        self.exam_progress.setFixedHeight(12)
        layout.addWidget(self.exam_progress)
        layout.addSpacing(15)

        # Question panel
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)

        self.lbl_q_domain = QLabel("Domain: ")
        self.lbl_q_domain.setStyleSheet("color: #94a3b8; font-style: italic;")

        self.lbl_q_text = QLabel("Question stem goes here.")
        self.lbl_q_text.setWordWrap(True)
        self.lbl_q_text.setStyleSheet("font-size: 16px; font-weight: 500; color: #f8fafc;")

        self.scroll_layout.addWidget(self.lbl_q_domain)
        self.scroll_layout.addWidget(self.lbl_q_text)
        self.scroll_layout.addSpacing(15)

        # Options Container Layout
        self.options_layout = QVBoxLayout()
        self.scroll_layout.addLayout(self.options_layout)
        self.scroll_layout.addSpacing(20)

        # Explanation / Feedback Area
        self.feedback_box = QGroupBox("Answer Evaluation")
        self.feedback_box.setStyleSheet("QGroupBox { font-weight: bold; color: #38bdf8; border: 1px solid #334155; border-radius: 8px; margin-top: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }")
        feedback_layout = QVBoxLayout(self.feedback_box)
        self.lbl_feedback_status = QLabel("")
        self.lbl_feedback_status.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.lbl_explanation = QLabel("")
        self.lbl_explanation.setWordWrap(True)
        self.lbl_explanation.setStyleSheet("color: #94a3b8;")

        feedback_layout.addWidget(self.lbl_feedback_status)
        feedback_layout.addWidget(self.lbl_explanation)
        self.scroll_layout.addWidget(self.feedback_box)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        layout.addSpacing(15)

        # Bottom navigation control layout
        nav_layout = QHBoxLayout()
        self.btn_quit_exam = QPushButton("Quit (Discard Session)")
        self.btn_quit_exam.setStyleSheet("QPushButton { background-color: #450a0a; color: #fca5a5; }")
        self.btn_quit_exam.clicked.connect(self.quit_exam_session)

        self.btn_save_exam = QPushButton("Save & Exit Session")
        self.btn_save_exam.clicked.connect(self.save_current_exam_state)

        self.btn_skip = QPushButton("Skip Question")
        self.btn_skip.clicked.connect(self.skip_question)

        self.btn_action = QPushButton("Submit Answer")
        self.btn_action.setObjectName("primaryBtn")
        self.btn_action.clicked.connect(self.on_exam_action)

        nav_layout.addWidget(self.btn_quit_exam)
        nav_layout.addWidget(self.btn_save_exam)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_skip)
        nav_layout.addWidget(self.btn_action)
        layout.addLayout(nav_layout)

        self.central_stack.addWidget(widget)

    def build_results_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(45, 45, 45, 45)

        lbl = QLabel("Exam Results Analysis")
        lbl.setObjectName("headerTitle")
        layout.addWidget(lbl)

        self.lbl_result_sub = QLabel("Time taken: --")
        self.lbl_result_sub.setObjectName("headerSubtitle")
        layout.addWidget(self.lbl_result_sub)
        layout.addSpacing(25)

        # Score display details
        score_card = QFrame()
        score_card.setObjectName("card")
        score_layout = QVBoxLayout(score_card)
        score_layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_result_score = QLabel("Score: --%")
        self.lbl_result_score.setStyleSheet("font-size: 28px; font-weight: 800; text-align: center;")
        self.lbl_result_score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_result_verdict = QLabel("Verdict info")
        self.lbl_result_verdict.setStyleSheet("font-size: 16px; font-weight: bold; text-align: center;")
        self.lbl_result_verdict.setAlignment(Qt.AlignmentFlag.AlignCenter)

        score_layout.addWidget(self.lbl_result_score)
        score_layout.addWidget(self.lbl_result_verdict)
        layout.addWidget(score_card)
        layout.addSpacing(20)

        # Domain breakdown list
        lbl_sec = QLabel("Performance Breakdown by Domain")
        lbl_sec.setObjectName("sectionTitle")
        layout.addWidget(lbl_sec)

        self.results_scroll = QScrollArea()
        self.results_scroll_content = QWidget()
        self.results_scroll_layout = QVBoxLayout(self.results_scroll_content)
        self.results_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.results_scroll.setWidget(self.results_scroll_content)
        self.results_scroll.setWidgetResizable(True)
        layout.addWidget(self.results_scroll)
        layout.addSpacing(20)

        # Return / Review buttons
        btn_layout = QHBoxLayout()
        btn_hub = QPushButton("Return to Main Hub")
        btn_hub.setObjectName("primaryBtn")
        btn_hub.clicked.connect(self.show_hub)

        self.btn_review_incorrect = QPushButton("Review Incorrect Answers")
        self.btn_review_incorrect.clicked.connect(self.review_incorrect_answers)

        self.btn_review_all = QPushButton("Review All Questions")
        self.btn_review_all.clicked.connect(self.review_all_questions)

        btn_layout.addWidget(btn_hub)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_review_incorrect)
        btn_layout.addWidget(self.btn_review_all)
        layout.addLayout(btn_layout)

        self.central_stack.addWidget(widget)

    def build_resume_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)

        lbl = QLabel("Saved Sessions")
        lbl.setObjectName("headerTitle")
        layout.addWidget(lbl)
        layout.addSpacing(20)

        self.save_list = QListWidget()
        layout.addWidget(self.save_list)
        layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Back to Hub")
        btn_back.clicked.connect(self.show_hub)

        self.btn_delete_save = QPushButton("Delete Save")
        self.btn_delete_save.setObjectName("dangerBtn")
        self.btn_delete_save.clicked.connect(self.delete_save_state)

        btn_resume = QPushButton("Resume Selected Session")
        btn_resume.setObjectName("primaryBtn")
        btn_resume.clicked.connect(self.resume_selected_exam)

        btn_layout.addWidget(btn_back)
        btn_layout.addWidget(self.btn_delete_save)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_resume)
        layout.addLayout(btn_layout)

        self.central_stack.addWidget(widget)

    # ─────────────────────────────────────────────
    #  Hub Logic / Refresh Dashboard
    # ─────────────────────────────────────────────
    def show_hub(self):
        self.current_course = None
        self.questions_list = []
        self.current_q_idx = 0
        self.elapsed_timer = 0
        self.timer_obj.stop()
        self.loaded_save_name = None

        history = load_history()

        # Update stats
        total_taken = len(history)
        self.lbl_total_taken.setText(f"Total Exams Attempted: {total_taken}")

        if total_taken > 0:
            passed = sum(1 for entry in history if entry.get("passed", False))
            pass_rate = (passed / total_taken) * 100
            avg_score = sum(entry.get("pct", 0.0) for entry in history) / total_taken
            self.lbl_pass_rate.setText(f"Average Pass Rate: {pass_rate:.1f}% ({passed}/{total_taken} passed)")
            self.lbl_avg_score.setText(f"Average Exam Score: {avg_score:.1f}%")
        else:
            self.lbl_pass_rate.setText("Average Pass Rate: 0.0%")
            self.lbl_avg_score.setText("Average Exam Score: 0.0%")

        # Clear scroll area domain details
        for i in reversed(range(self.domains_scroll_layout.count())):
            self.domains_scroll_layout.itemAt(i).widget().setParent(None)

        # Compile objective domain analytics
        domain_totals = {}
        for entry in history:
            for d, counts in entry.get("domain_results", {}).items():
                if d not in domain_totals:
                    domain_totals[d] = {"correct": 0, "total": 0}
                domain_totals[d]["correct"] += counts.get("correct", 0)
                domain_totals[d]["total"] += counts.get("total", 0)

        for d, counts in sorted(domain_totals.items()):
            d_pct = (counts["correct"] / counts["total"] * 100) if counts["total"] else 0
            label = d.split("·")[1].strip() if "·" in d else d

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 4, 0, 4)

            lbl_name = QLabel(label)
            lbl_name.setStyleSheet("font-weight: 500; font-size: 12px;")

            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(int(d_pct))
            progress.setFormat(f"{d_pct:.0f}% ({counts['correct']}/{counts['total']})")
            progress.setFixedWidth(220)
            progress.setFixedHeight(18)

            # Apply domain threshold color code dynamically
            if d_pct >= 75:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #22c55e; }")
            elif d_pct >= 50:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #eab308; }")
            else:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #ef4444; }")

            row_layout.addWidget(lbl_name)
            row_layout.addWidget(progress)
            self.domains_scroll_layout.addWidget(row)

        self.central_stack.setCurrentIndex(0)

    # ─────────────────────────────────────────────
    #  Course Select & Config Logic
    # ─────────────────────────────────────────────
    def show_course_select(self):
        self.course_list.clear()
        courses = discover_courses()
        for c in courses:
            item = QListWidgetItem(f"{c.get('short_title')} ({(len(c.get('questions', [])))} Qs)")
            item.setData(Qt.ItemDataRole.UserRole, c["_path"])
            self.course_list.addItem(item)
        self.central_stack.setCurrentIndex(1)

    def go_to_mode_select(self):
        current_item = self.course_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No course selected", "Please select an exam from the list to continue.")
            return

        course_path = current_item.data(Qt.ItemDataRole.UserRole)
        try:
            self.current_course = load_course(course_path)
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Could not load course JSON: {e}")
            return

        # Setup configuration options
        self.lbl_mode_title.setText(f"Configure Mode: {self.current_course.short_title}")

        # Refresh domain selections if dynamic
        self.combo_domain.clear()
        for d in self.current_course.domains:
            self.combo_domain.addItem(d)

        self.combo_mode.setCurrentIndex(0)
        self.on_mode_changed(0)
        self.central_stack.setCurrentIndex(2)

    def on_mode_changed(self, idx):
        # Clear specific widgets layout
        for i in reversed(range(self.mode_options_layout.count())):
            widget = self.mode_options_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if idx == 2:  # Quick Drill
            self.spin_count.setMaximum(len(self.current_course.questions))
            self.mode_options_layout.addWidget(self.spin_count_lbl)
            self.mode_options_layout.addWidget(self.spin_count)
        elif idx == 3:  # Domain Focus
            self.mode_options_layout.addWidget(self.combo_domain_lbl)
            self.mode_options_layout.addWidget(self.combo_domain)

    def start_new_exam(self):
        mode_idx = self.combo_mode.currentIndex()
        questions = list(self.current_course.questions)

        if mode_idx == 1:  # Shuffled
            random.shuffle(questions)
        elif mode_idx == 2:  # Quick drill
            random.shuffle(questions)
            questions = questions[:self.spin_count.value()]
        elif mode_idx == 3:  # Domain focus
            target_domain = self.combo_domain.currentText()
            questions = [q for q in questions if q.domain == target_domain]
            random.shuffle(questions)

        self.questions_list = questions
        self.current_q_idx = 0
        self.elapsed_timer = 0
        self.loaded_save_name = None

        self.start_exam_session()

    # ─────────────────────────────────────────────
    #  Exam Gameplay Screen Actions
    # ─────────────────────────────────────────────
    def start_exam_session(self):
        self.central_stack.setCurrentIndex(3)
        self.timer_obj.start(1000)
        self.load_question(self.current_q_idx)

    def update_timer(self):
        self.elapsed_timer += 1
        h, m = divmod(self.elapsed_timer, 3600)
        m, s = divmod(m, 60)
        self.lbl_timer.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def load_question(self, idx):
        self.current_q_idx = idx
        q = self.questions_list[idx]

        # Reset UI element states
        self.btn_flag.setChecked(q.flagged)
        self.lbl_exam_title.setText(f"{self.current_course.short_title}")
        self.lbl_q_domain.setText(f"Domain: {q.domain}")
        self.lbl_q_text.setText(f"<b>Q{q.number}.</b> {q.text}")

        # Update progress bar
        self.exam_progress.setRange(0, len(self.questions_list))
        self.exam_progress.setValue(idx)
        self.exam_progress.setFormat(f"Question {idx+1} of {len(self.questions_list)}")

        # Clear active options layout
        for i in reversed(range(self.options_layout.count())):
            self.options_layout.itemAt(i).widget().setParent(None)

        self.option_widgets = {}
        for opt in q.options:
            card = OptionCard(opt["key"], opt["text"])
            card.clicked_callback = self.on_option_clicked
            self.options_layout.addWidget(card)
            self.option_widgets[opt["key"]] = card

        # Evaluate layout state depending on whether it has already been answered
        if q.user_answer is not None:
            # Re-draw answered state
            for key, card in self.option_widgets.items():
                if key == q.correct:
                    card.set_state("correct")
                elif key == q.user_answer:
                    card.set_state("incorrect")
            self.lbl_feedback_status.setText("Question Answered")
            if q.user_answer == q.correct:
                self.lbl_feedback_status.setStyleSheet("color: #22c55e; font-weight: bold;")
            else:
                self.lbl_feedback_status.setStyleSheet("color: #ef4444; font-weight: bold;")
            self.lbl_explanation.setText(q.explanation)
            self.feedback_box.show()
            self.btn_skip.setEnabled(False)
            self.btn_action.setText("Next Question" if idx + 1 < len(self.questions_list) else "Finish Exam")
            self.btn_action.setEnabled(True)
        else:
            self.feedback_box.hide()
            self.btn_skip.setEnabled(True)
            self.btn_action.setText("Submit Answer")
            self.btn_action.setEnabled(False)

        self.question_start_time = time.time()

    def on_option_clicked(self, key):
        q = self.questions_list[self.current_q_idx]
        if q.user_answer is not None:
            return  # Already evaluated

        # Toggle highlights visual state
        for o_key, card in self.option_widgets.items():
            if o_key == key:
                card.set_state("selected")
                self.selected_key = key
                self.btn_action.setEnabled(True)
            else:
                card.set_state("default")

    def on_exam_action(self):
        q = self.questions_list[self.current_q_idx]

        if q.user_answer is None:
            # Submit Answer state
            q.user_answer = self.selected_key
            q.time_spent += time.time() - self.question_start_time

            # Update option card visuals
            for key, card in self.option_widgets.items():
                if key == q.correct:
                    card.set_state("correct")
                elif key == q.user_answer:
                    card.set_state("incorrect")

            # Setup feedbacks
            if q.user_answer == q.correct:
                self.lbl_feedback_status.setText("✔ Correct")
                self.lbl_feedback_status.setStyleSheet("color: #22c55e; font-weight: bold;")
            else:
                self.lbl_feedback_status.setText(f"✘ Incorrect (Correct Answer: {q.correct})")
                self.lbl_feedback_status.setStyleSheet("color: #ef4444; font-weight: bold;")

            self.lbl_explanation.setText(q.explanation)
            self.feedback_box.show()
            self.btn_skip.setEnabled(False)
            self.btn_action.setText("Next Question" if self.current_q_idx + 1 < len(self.questions_list) else "Finish Exam")
        else:
            # Advance index
            if self.current_q_idx + 1 < len(self.questions_list):
                self.load_question(self.current_q_idx + 1)
            else:
                self.evaluate_final_results()

    def skip_question(self):
        # Cycle index to next unanswered question
        q = self.questions_list[self.current_q_idx]
        q.time_spent += time.time() - self.question_start_time

        # Find next unanswered question index
        next_idx = None
        for offset in range(1, len(self.questions_list)):
            candidate = (self.current_q_idx + offset) % len(self.questions_list)
            if self.questions_list[candidate].user_answer is None:
                next_idx = candidate
                break

        if next_idx is not None:
            self.load_question(next_idx)
        else:
            QMessageBox.information(self, "No skipped questions", "All questions have already been answered.")

    def toggle_flag(self):
        q = self.questions_list[self.current_q_idx]
        q.flagged = self.btn_flag.isChecked()

    # ─────────────────────────────────────────────
    #  Quit & State Save Integrations
    # ─────────────────────────────────────────────
    def quit_exam_session(self):
        reply = QMessageBox.question(
            self, "Discard Progress",
            "Are you sure you want to quit this exam session? Current run logs will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.show_hub()

    def save_current_exam_state(self):
        suggested_name = f"{self.current_course.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        name, ok = QMessageBox.question(
            self, "Save Session State",
            "Would you like to save this active exam and continue later?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if ok == QMessageBox.StandardButton.Yes:
            # Save State Data structure matching CLI Engine
            state_file = SAVES_DIR / f"{suggested_name}.json"
            state_data = {
                "course_id": self.current_course.id,
                "course_title": self.current_course.title,
                "course_short_title": self.current_course.short_title,
                "passing_score": self.current_course.passing_score,
                "domains": self.current_course.domains,
                "scoring_guide": self.current_course.scoring_guide,
                "elapsed_time": float(self.elapsed_timer),
                "timestamp": datetime.now().isoformat(),
                "questions": [asdict(q) for q in self.questions_list]
            }
            try:
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(state_data, f, indent=2)

                # Clean up loaded save name if overwriting/resuming
                if self.loaded_save_name:
                    p = SAVES_DIR / f"{self.loaded_save_name}.json"
                    if p.exists():
                        p.unlink()

                QMessageBox.information(self, "State Saved", "Your exam progress has been saved. Returning to Hub.")
                self.show_hub()
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save progress file: {e}")

    # ─────────────────────────────────────────────
    #  Results & Learner Analytics Logs
    # ─────────────────────────────────────────────
    def evaluate_final_results(self):
        self.timer_obj.stop()
        self.central_stack.setCurrentIndex(4)

        correct_qs = [q for q in self.questions_list if q.user_answer == q.correct]
        n_total = len(self.questions_list)
        score = len(correct_qs)
        pct = (score / n_total * 100) if n_total else 0.0
        passed = score >= self.current_course.passing_score

        verdict = self.current_course.verdict(score)
        vcol = self.current_course.verdict_color(score)

        # Clear old result cards
        for i in reversed(range(self.results_scroll_layout.count())):
            self.results_scroll_layout.itemAt(i).widget().setParent(None)

        h, m = divmod(self.elapsed_timer, 3600)
        m, s = divmod(m, 60)
        time_str = f"{h:02d}h {m:02d}m {s:02d}s" if h else f"{m:02d}m {s:02d}s"
        self.lbl_result_sub.setText(f"Time taken: {time_str}  •  Passing threshold: {self.current_course.passing_score}/{n_total} correct")

        self.lbl_result_score.setText(f"{score} / {n_total} ({pct:.1f}%)")
        self.lbl_result_score.setStyleSheet(f"font-size: 32px; font-weight: 800; color: {vcol};")
        self.lbl_result_verdict.setText(verdict)
        self.lbl_result_verdict.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {vcol};")

        # Compile domain-level stats for database logs
        domain_results = {}
        domains_in_set = list(dict.fromkeys(q.domain for q in self.questions_list))
        for d in domains_in_set:
            d_qs = [q for q in self.questions_list if q.domain == d]
            d_correct = [q for q in d_qs if q.user_answer == q.correct]
            d_pct = len(d_correct) / len(d_qs) * 100 if d_qs else 0

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 5, 0, 5)

            lbl_name = QLabel(d.split("·")[1].strip() if "·" in d else d)
            progress = QProgressBar()
            progress.setRange(0, 100)
            progress.setValue(int(d_pct))
            progress.setFormat(f"{d_pct:.0f}% ({len(d_correct)}/{len(d_qs)})")
            progress.setFixedWidth(200)
            progress.setFixedHeight(18)

            if d_pct >= 75:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #22c55e; }")
            elif d_pct >= 50:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #eab308; }")
            else:
                progress.setStyleSheet("QProgressBar::chunk { background-color: #ef4444; }")

            row_layout.addWidget(lbl_name)
            row_layout.addWidget(progress)
            self.results_scroll_layout.addWidget(row)

            domain_results[d] = {"correct": len(d_correct), "total": len(d_qs)}

        # Log completion details to performance history
        history = load_history()
        history.append({
            "course_id": self.current_course.id,
            "course_short_title": self.current_course.short_title,
            "score": score,
            "total_questions": n_total,
            "pct": pct,
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "elapsed": float(self.elapsed_timer),
            "domain_results": domain_results
        })
        save_history(history)

        # Delete active state if exam completed successfully
        if self.loaded_save_name:
            p = SAVES_DIR / f"{self.loaded_save_name}.json"
            if p.exists():
                p.unlink()

    # ─────────────────────────────────────────────
    #  Saved Session Resume Picker Layout
    # ─────────────────────────────────────────────
    def show_resume_picker(self):
        self.save_list.clear()
        states = load_exam_states()
        for s in states:
            ts = datetime.fromisoformat(s.get("timestamp", "")).strftime("%Y-%m-%d %H:%M")
            answered = sum(1 for q in s.get("questions", []) if q.get("user_answer") is not None)
            item_lbl = f"{s.get('course_short_title')}  ({answered}/{len(s.get('questions', []))} Qs)  •  Saved: {ts}"
            item = QListWidgetItem(item_lbl)
            item.setData(Qt.ItemDataRole.UserRole, s["_filename"])
            self.save_list.addItem(item)

        self.central_stack.setCurrentIndex(5)

    def resume_selected_exam(self):
        current_item = self.save_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No session selected", "Please select a saved exam from the list to continue.")
            return

        filename = current_item.data(Qt.ItemDataRole.UserRole)
        state_file = SAVES_DIR / f"{filename}.json"

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)

            # Reconstruct course structure
            self.current_course = Course(
                id=state["course_id"],
                title=state["course_title"],
                short_title=state["course_short_title"],
                passing_score=state["passing_score"],
                description="",
                domains=state["domains"],
                scoring_guide=state["scoring_guide"],
                questions=[]
            )

            # Reconstruct question elements
            self.questions_list = []
            for q in state["questions"]:
                self.questions_list.append(Question(
                    number=q["number"],
                    domain=q["domain"],
                    text=q["text"],
                    options=q["options"],
                    correct=q["correct"],
                    explanation=q["explanation"],
                    user_answer=q["user_answer"],
                    flagged=q["flagged"],
                    time_spent=q["time_spent"]
                ))
            self.current_course.questions = self.questions_list
            self.elapsed_timer = int(state.get("elapsed_time", 0.0))
            self.loaded_save_name = filename

            # Find first unanswered index
            start_q = 0
            for idx, q in enumerate(self.questions_list):
                if q.user_answer is None:
                    start_q = idx
                    break

            self.start_exam_session()
            self.load_question(start_q)

        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Could not load state file: {e}")

    def delete_save_state(self):
        current_item = self.save_list.currentItem()
        if not current_item:
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this saved state?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            p = SAVES_DIR / f"{filename}.json"
            if p.exists():
                p.unlink()
            self.show_resume_picker()

    # ─────────────────────────────────────────────
    #  JSON Import Actions
    # ─────────────────────────────────────────────
    def import_course_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Exam JSON Configuration", "", "JSON files (*.json)")
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate structural bounds
            required = ["id", "title", "domains", "questions"]
            for r in required:
                if r not in data:
                    raise KeyError(f"Missing required metadata object: '{r}'")

            for idx, q in enumerate(data["questions"]):
                for sub in ["number", "domain", "text", "options", "correct", "explanation"]:
                    if sub not in q:
                        raise KeyError(f"Question index {idx} is missing required data field: '{sub}'")

            target_path = COURSES_DIR / f"{data['id']}.json"
            shutil.copy(file_path, target_path)

            QMessageBox.information(self, "Import Successful", f"Course '{data.get('short_title', data['title'])}' imported successfully.")
            self.show_hub()

        except Exception as e:
            QMessageBox.critical(self, "Validation Error", f"Invalid course file structure: {e}")

    # ─────────────────────────────────────────────
    #  Clear history helper
    # ─────────────────────────────────────────────
    def clear_performance_data(self):
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "Are you sure you want to clear all history dashboard metrics?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            save_history([])
            self.show_hub()

    # ─────────────────────────────────────────────
    #  Exam Review Screen Implementations
    # ─────────────────────────────────────────────
    def review_incorrect_answers(self):
        incorrect_qs = [q for q in self.questions_list if q.user_answer != q.correct]
        if not incorrect_qs:
            QMessageBox.information(self, "Clean Sheet", "Congratulations, you had no incorrect answers!")
            return
        self.launch_review_window(incorrect_qs, "Incorrect Answers Review")

    def review_all_questions(self):
        self.launch_review_window(self.questions_list, "Review All Questions")

    def launch_review_window(self, questions_to_review, title):
        self.review_qs = questions_to_review
        self.review_idx = 0

        # Build dialog window dynamically
        self.review_win = QWidget(self, Qt.WindowType.Window)
        self.review_win.setWindowTitle(title)
        self.review_win.resize(800, 600)
        self.review_win.setStyleSheet(QSS_THEME)

        layout = QVBoxLayout(self.review_win)
        layout.setContentsMargins(25, 25, 25, 25)

        self.lbl_rev_header = QLabel("Review Stem Title")
        self.lbl_rev_header.setObjectName("sectionTitle")
        layout.addWidget(self.lbl_rev_header)

        # Question scroll layout
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.rev_layout = QVBoxLayout(scroll_content)

        self.lbl_rev_domain = QLabel("Domain: ")
        self.lbl_rev_domain.setStyleSheet("color: #94a3b8; font-style: italic;")
        self.lbl_rev_q_text = QLabel("")
        self.lbl_rev_q_text.setWordWrap(True)
        self.lbl_rev_q_text.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc;")

        self.rev_layout.addWidget(self.lbl_rev_domain)
        self.rev_layout.addWidget(self.lbl_rev_q_text)
        self.rev_layout.addSpacing(15)

        self.rev_options_layout = QVBoxLayout()
        self.rev_layout.addLayout(self.rev_options_layout)
        self.rev_layout.addSpacing(15)

        self.rev_feedback_box = QGroupBox("Answer Explanations")
        self.rev_feedback_box.setStyleSheet("QGroupBox { font-weight: bold; color: #38bdf8; border: 1px solid #334155; border-radius: 8px; margin-top: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }")
        rev_f_layout = QVBoxLayout(self.rev_feedback_box)
        self.lbl_rev_status = QLabel("")
        self.lbl_rev_status.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.lbl_rev_exp = QLabel("")
        self.lbl_rev_exp.setWordWrap(True)
        self.lbl_rev_exp.setStyleSheet("color: #94a3b8;")
        rev_f_layout.addWidget(self.lbl_rev_status)
        rev_f_layout.addWidget(self.lbl_rev_exp)

        self.rev_layout.addWidget(self.rev_feedback_box)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        layout.addSpacing(15)

        # Nav bar
        nav = QHBoxLayout()
        self.btn_rev_prev = QPushButton("Previous")
        self.btn_rev_prev.clicked.connect(self.prev_rev_question)
        self.btn_rev_next = QPushButton("Next")
        self.btn_rev_next.clicked.connect(self.next_rev_question)
        btn_close = QPushButton("Close Review")
        btn_close.clicked.connect(self.review_win.close)

        nav.addWidget(self.btn_rev_prev)
        nav.addWidget(self.btn_rev_next)
        nav.addStretch()
        nav.addWidget(btn_close)
        layout.addLayout(nav)

        self.load_rev_question(0)
        self.review_win.show()

    def load_rev_question(self, idx):
        self.review_idx = idx
        q = self.review_qs[idx]

        self.lbl_rev_header.setText(f"Question {idx + 1} of {len(self.review_qs)} (Internal Q#{q.number})")
        self.lbl_rev_domain.setText(f"Domain: {q.domain}")
        self.lbl_rev_q_text.setText(q.text)

        # Clear layout
        for i in reversed(range(self.rev_options_layout.count())):
            self.rev_options_layout.itemAt(i).widget().setParent(None)

        for opt in q.options:
            card = OptionCard(opt["key"], opt["text"])
            if opt["key"] == q.correct:
                card.set_state("correct")
            elif opt["key"] == q.user_answer:
                card.set_state("incorrect")
            self.rev_options_layout.addWidget(card)

        if q.user_answer == q.correct:
            self.lbl_rev_status.setText("✔ Answered Correctly")
            self.lbl_rev_status.setStyleSheet("color: #22c55e; font-weight: bold;")
        else:
            given = q.option_text(q.user_answer)
            self.lbl_rev_status.setText(f"✘ Incorrect (Your Choice: {q.user_answer}  •  Correct: {q.correct})")
            self.lbl_rev_status.setStyleSheet("color: #ef4444; font-weight: bold;")

        self.lbl_rev_exp.setText(q.explanation)

        self.btn_rev_prev.setEnabled(idx > 0)
        self.btn_rev_next.setEnabled(idx + 1 < len(self.review_qs))

    def prev_rev_question(self):
        if self.review_idx > 0:
            self.load_rev_question(self.review_idx - 1)

    def next_rev_question(self):
        if self.review_idx + 1 < len(self.review_qs):
            self.load_rev_question(self.review_idx + 1)


# ─────────────────────────────────────────────
#  Application Entrance Point
# ─────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    
    # Modern Dark slate Palette setup
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0b0f19"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#f1f5f9"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#0f172a"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1e293b"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#f1f5f9"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#f1f5f9"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#f1f5f9"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#1e293b"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#f1f5f9"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#38bdf8"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#0284c7"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    win = ExamApp()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
