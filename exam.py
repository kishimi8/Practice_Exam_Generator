#!/usr/bin/env python3
"""
Certification Practice Exam Engine
─────────────────────────────────────────────
An interactive terminal interface featuring:
- Course selector
- Exam state save & resume
- Course import (JSON files)
- Performance dashboard with learner analytics
"""

import sys
import time
import random
import os
import json
import textwrap
import shutil
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

# ─────────────────────────────────────────────
#  Paths & Persistence Setup
# ─────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
COURSES_DIR = SCRIPT_DIR / "courses"
SAVES_DIR = SCRIPT_DIR / "saves"
HISTORY_FILE = SCRIPT_DIR / "history.json"

COURSES_DIR.mkdir(exist_ok=True)
SAVES_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
#  ANSI colour helpers
# ─────────────────────────────────────────────
def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

USE_COLOR = _supports_color()

class C:
    RESET   = "\033[0m"   if USE_COLOR else ""
    BOLD    = "\033[1m"   if USE_COLOR else ""
    DIM     = "\033[2m"   if USE_COLOR else ""
    RED     = "\033[91m"  if USE_COLOR else ""
    GREEN   = "\033[92m"  if USE_COLOR else ""
    YELLOW  = "\033[93m"  if USE_COLOR else ""
    BLUE    = "\033[94m"  if USE_COLOR else ""
    MAGENTA = "\033[95m"  if USE_COLOR else ""
    CYAN    = "\033[96m"  if USE_COLOR else ""

def bold(s):    return f"{C.BOLD}{s}{C.RESET}"
def dim(s):     return f"{C.DIM}{s}{C.RESET}"
def red(s):     return f"{C.RED}{s}{C.RESET}"
def green(s):   return f"{C.GREEN}{s}{C.RESET}"
def yellow(s):  return f"{C.YELLOW}{s}{C.RESET}"
def cyan(s):    return f"{C.CYAN}{s}{C.RESET}"
def magenta(s): return f"{C.MAGENTA}{s}{C.RESET}"
def blue(s):    return f"{C.BLUE}{s}{C.RESET}"

WIDTH = 72

def rule(char="─", color=C.DIM):
    return f"{color}{char * WIDTH}{C.RESET}"

def center(text, total=WIDTH):
    return text.center(total)

# ─────────────────────────────────────────────
#  Data Models
# ─────────────────────────────────────────────
@dataclass
class Question:
    number: int
    domain: str
    text: str
    options: list          # [{"key": "A", "text": "..."}]
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
    scoring_guide: list[dict]   # [{"min": int, "label": str}]
    questions: list[Question]

    def verdict(self, score: int) -> str:
        for tier in sorted(self.scoring_guide, key=lambda t: t["min"], reverse=True):
            if score >= tier["min"]:
                return tier["label"]
        return self.scoring_guide[-1]["label"]

    def verdict_color(self, score: int) -> str:
        n = len(self.questions)
        pct = score / n * 100 if n else 0
        if pct >= 90:  return green
        if pct >= 75:  return yellow
        return red


# ─────────────────────────────────────────────
#  Helpers & Persist Functions
# ─────────────────────────────────────────────
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


def discover_courses() -> list[tuple[str, Path]]:
    if not COURSES_DIR.exists():
        return []
    courses = []
    for p in sorted(COURSES_DIR.glob("*.json")):
        try:
            with open(p, encoding="utf-8") as f:
                meta = json.load(f)
            courses.append((meta.get("short_title", p.stem), p))
        except Exception:
            pass
    return courses


def load_history() -> List[Dict[str, Any]]:
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("history", [])
    except Exception:
        return []


def save_history(history: List[Dict[str, Any]]):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": history}, f, indent=2)
    except Exception as e:
        print(red(f"Error saving history: {e}"))


def save_exam_state(course: Course, questions: list[Question], elapsed_time: float, state_name: str):
    state_file = SAVES_DIR / f"{state_name}.json"
    state_data = {
        "course_id": course.id,
        "course_title": course.title,
        "course_short_title": course.short_title,
        "passing_score": course.passing_score,
        "domains": course.domains,
        "scoring_guide": course.scoring_guide,
        "elapsed_time": elapsed_time,
        "timestamp": datetime.now().isoformat(),
        "questions": [asdict(q) for q in questions]
    }
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2)
        print(green(f"\n  Exam state saved successfully: {state_file.name}"))
    except Exception as e:
        print(red(f"\n  Failed to save state: {e}"))


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


def delete_exam_state(state_name: str):
    p = SAVES_DIR / f"{state_name}.json"
    if p.exists():
        p.unlink()


# ─────────────────────────────────────────────
#  Interactive Menus & UI
# ─────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause(prompt="  Press Enter to continue..."):
    try:
        input(f"\n{dim(prompt)}")
    except (KeyboardInterrupt, EOFError):
        pass


def fmt_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m:02d}m {s:02d}s"


def progress_bar(current, total, width=38):
    filled = int(width * current / total) if total else 0
    bar = "\u2588" * filled + "\u2591" * (width - filled)
    pct = current / total * 100 if total else 0
    return f"{cyan(bar)} {yellow(f'{pct:.0f}%')} ({current}/{total})"


def print_header(title, subtitle=""):
    print()
    print(rule("=", C.CYAN + C.BOLD))
    print(bold(cyan(center(title))))
    if subtitle:
        print(dim(center(subtitle)))
    print(rule("=", C.CYAN + C.BOLD))


def prompt_choice(valid: list[str], prompt: str = "  Your choice: ") -> str:
    valid_up = [v.upper() for v in valid]
    while True:
        try:
            ans = input(f"\n{cyan(prompt)}").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)
        if ans in valid_up:
            return ans
        print(red(f"  Invalid choice. Options: {', '.join(valid_up)}"))


def get_yn(prompt: str) -> bool:
    while True:
        try:
            ans = input(f"  {cyan(prompt)} [y/n]: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False


# ─────────────────────────────────────────────
#  Feature 1: Course Import
# ─────────────────────────────────────────────
def import_course_menu():
    clear()
    print_header("Import Course File", "Add a custom practice exam JSON file")
    print("\n  The JSON file must follow the standard exam configuration structure.")
    print("  Specify the absolute or relative path to the JSON file.\n")

    try:
        path_str = input(cyan("  Enter path to course JSON file (or press enter to cancel): ")).strip()
        if not path_str:
            return
        path = Path(path_str).resolve()
        if not path.exists():
            print(red(f"\n  Error: File not found at path: {path}"))
            pause()
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Simple validation
        required_fields = ["id", "title", "domains", "questions"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            print(red(f"\n  Validation Error: Missing required top-level field(s): {', '.join(missing)}"))
            pause()
            return

        # Check questions schema
        for idx, q in enumerate(data["questions"]):
            for q_field in ["number", "domain", "text", "options", "correct", "explanation"]:
                if q_field not in q:
                    print(red(f"\n  Validation Error in question index {idx}: missing '{q_field}'"))
                    pause()
                    return

        # Write to courses directory
        target_path = COURSES_DIR / f"{data['id']}.json"
        shutil.copy(path, target_path)
        print(green(f"\n  Success! Course '{data.get('short_title', data['title'])}' imported successfully."))
        pause()

    except Exception as e:
        print(red(f"\n  Failed to import course: {e}"))
        pause()


# ─────────────────────────────────────────────
#  Feature 2: Performance Dashboard
# ─────────────────────────────────────────────
def performance_dashboard_menu():
    clear()
    history = load_history()
    print_header("Learner Performance Dashboard", f"Total Exams Taken: {len(history)}")

    if not history:
        print("\n" + center("No performance history found yet."))
        print(center(dim("Complete an exam to log your statistics here!")))
        pause()
        return

    # Aggregate Analytics
    total_taken = len(history)
    passed_count = sum(1 for entry in history if entry.get("passed", False))
    pass_rate = (passed_count / total_taken) * 100
    avg_score = sum(entry.get("pct", 0.0) for entry in history) / total_taken

    # Domain strengths breakdown
    domain_totals = {}  # {domain_name: {"correct": x, "total": y}}
    for entry in history:
        for domain, results in entry.get("domain_results", {}).items():
            if domain not in domain_totals:
                domain_totals[domain] = {"correct": 0, "total": 0}
            domain_totals[domain]["correct"] += results.get("correct", 0)
            domain_totals[domain]["total"] += results.get("total", 0)

    print()
    print(f"  {bold('Summary statistics:')}")
    print(f"    - Pass Rate:           {bold(green(f'{pass_rate:.1f}%'))} ({passed_count}/{total_taken} passed)")
    print(f"    - Average Score:       {bold(cyan(f'{avg_score:.1f}%'))}")
    print(f"    - Total Questions:     {sum(entry.get('total_questions', 0) for entry in history)} attempted")
    print()
    print(rule())

    # Domain Strengths Breakdown
    print(f"\n  {bold(yellow('Overall Domain Strengths:'))}\n")
    for d, counts in sorted(domain_totals.items()):
        d_pct = (counts["correct"] / counts["total"] * 100) if counts["total"] else 0
        bar_len = 20
        filled = int(bar_len * d_pct / 100)
        bar = "\u2588" * filled + "\u2591" * (bar_len - filled)
        col = green if d_pct >= 75 else (yellow if d_pct >= 50 else red)
        label = d.split("·")[1].strip() if "·" in d else d
        c_val = counts.get('correct', 0)
        t_val = counts.get('total', 0)
        print(f"  {col(bar)}  {col(f'{d_pct:5.1f}%')}  {bold(f'{c_val}/{t_val}')}  {dim(label)}")

    print()
    print(rule())

    # Last 5 Attempts
    print(f"\n  {bold('Recent Exam Attempts:')}\n")
    for entry in reversed(history[-5:]):
        ts = datetime.fromisoformat(entry.get("timestamp", "")).strftime("%Y-%m-%d %H:%M")
        status = green("PASS") if entry.get("passed", False) else red("FAIL")
        score_val = entry.get('score', 0)
        t_qs = entry.get('total_questions', 0)
        print(f"    {dim(ts)}  |  {bold(entry['course_short_title']):<30}  |  Score: {bold(f'{score_val}/{t_qs}')} ({entry['pct']:.1f}%)  [{status}]")

    print()
    print(rule())
    print("\n  [D] Clear History Data  [B] Back to Hub")
    choice = prompt_choice(["D", "B"])
    if choice == "D":
        if get_yn("Are you sure you want to delete all historical logs?"):
            save_history([])
            print(green("\n  Performance logs cleared."))
            time.sleep(1)


# ─────────────────────────────────────────────
#  Feature 3: State Save & Resume Picker
# ─────────────────────────────────────────────
def save_and_quit_exam(course: Course, questions: list[Question], elapsed_time: float):
    clear()
    print_header("Save Exam Progress")
    print(f"\n  Saving progress for: {course.short_title}")
    answered_count = sum(1 for q in questions if q.user_answer is not None)
    print(f"  Currently answered: {answered_count}/{len(questions)} questions")
    print()

    filename_suggestion = f"{course.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    name = input(cyan(f"  Name this save state [{filename_suggestion}]: ")).strip()
    if not name:
        name = filename_suggestion

    save_exam_state(course, questions, elapsed_time, name)
    pause("\n  Your state is saved. Returning to hub...")
    sys.exit(0)


def resume_exam_picker() -> Optional[tuple[Course, list[Question], float, str]]:
    clear()
    states = load_exam_states()
    print_header("Resume Saved Exam", f"Found {len(states)} active saves")

    if not states:
        print("\n" + center("No saved exam progress states found."))
        pause()
        return None

    for i, s in enumerate(states, start=1):
        ts = datetime.fromisoformat(s.get("timestamp", "")).strftime("%Y-%m-%d %H:%M")
        qs = s.get("questions", [])
        ans = sum(1 for q in qs if q.get("user_answer") is not None)
        print(f"  {bold(str(i) + ')') } {s.get('course_short_title')}  {dim(f'({ans}/{len(qs)} Qs answered)')}  - Saved: {dim(ts)}")

    print()
    print("  [C] Cancel / Go back")
    nums = [str(i) for i in range(1, len(states) + 1)]
    choice = prompt_choice(nums + ["C"], f"Select save to resume (1-{len(states)}): ")
    if choice == "C":
        return None

    state = states[int(choice) - 1]

    # Reconstruct objects
    course = Course(
        id=state["course_id"],
        title=state["course_title"],
        short_title=state["course_short_title"],
        passing_score=state["passing_score"],
        description="",
        domains=state["domains"],
        scoring_guide=state["scoring_guide"],
        questions=[]
    )

    questions = []
    for q in state["questions"]:
        questions.append(Question(
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
    course.questions = questions

    return course, questions, state.get("elapsed_time", 0.0), state["_filename"]


# ─────────────────────────────────────────────
#  Course Selector
# ─────────────────────────────────────────────
def select_course() -> Course:
    available = discover_courses()

    if not available:
        print(red(
            f"\n  No course files found in: {COURSES_DIR}\n"
            "  Please use the Import Course option from the hub, or add a JSON file manually."
        ))
        pause()
        sys.exit(1)

    print()
    print(bold(yellow("  Available Courses:")))
    print()
    for i, (title, _) in enumerate(available, start=1):
        print(f"  {bold(str(i) + ')')} {title}")
    print()

    nums = [str(i) for i in range(1, len(available) + 1)]
    choice = prompt_choice(nums, f"Select a course (1-{len(available)}): ")
    _, path = available[int(choice) - 1]

    try:
        return load_course(path)
    except Exception as e:
        print(red(f"\n  Error loading course: {e}"))
        pause()
        sys.exit(1)


# ─────────────────────────────────────────────
#  Exam Execution Engine
# ─────────────────────────────────────────────
def mode_menu(course: Course) -> dict:
    n_total = len(course.questions)
    n_domains = len(course.domains)

    print()
    print(bold(yellow("  Select Exam Mode:")))
    print()
    print(f"  {bold('1)')} Full exam  – all {n_total} questions in order")
    print(f"  {bold('2)')} Full exam  – questions in random order")
    print(f"  {bold('3)')} Quick drill – choose how many questions")
    if n_domains > 1:
        print(f"  {bold('4)')} Domain focus – pick a single domain")
    print()

    valid_modes = ["1", "2", "3"] + (["4"] if n_domains > 1 else [])
    mode = prompt_choice(valid_modes, f"Select mode ({'/'.join(valid_modes)}): ")

    config = {"shuffle": False, "subset": None, "domain": None}

    if mode == "2":
        config["shuffle"] = True

    elif mode == "3":
        while True:
            try:
                n = int(input(f"  {cyan(f'How many questions? (1-{n_total}): ')}").strip())
                if 1 <= n <= n_total:
                    config["subset"] = n
                    config["shuffle"] = True
                    break
            except (ValueError, KeyboardInterrupt, EOFError):
                pass
            print(red(f"  Enter a number between 1 and {n_total}."))

    elif mode == "4":
        print()
        for i, d in enumerate(course.domains, start=1):
            count = sum(1 for q in course.questions if q.domain == d)
            print(f"  {bold(str(i) + ')')} {d}  {dim(f'({count} Qs)')}")
        print()
        nums = [str(i) for i in range(1, len(course.domains) + 1)]
        d_choice = prompt_choice(nums, f"Choose domain (1-{len(course.domains)}): ")
        config["domain"] = course.domains[int(d_choice) - 1]
        config["shuffle"] = get_yn("Shuffle questions?")

    return config


def build_question_list(course: Course, config: dict) -> list[Question]:
    import copy
    qs = copy.deepcopy(course.questions)

    if config.get("domain"):
        qs = [q for q in qs if q.domain == config["domain"]]

    if config.get("shuffle"):
        random.shuffle(qs)

    if config.get("subset"):
        qs = qs[: config["subset"]]

    return qs


def display_question(q: Question, idx: int, total: int, elapsed: float):
    clear()
    flag_str = f"  {yellow('>> FLAGGED')}" if q.flagged else ""
    print(rule())
    print(f"  {bold(cyan(f'Question {idx}/{total}'))}  {dim(f'#{q.number}')}"
          f"  {dim(q.domain)}  {dim(fmt_time(elapsed))}{flag_str}")
    print(f"  {progress_bar(idx - 1, total)}")
    print(rule())
    print()

    wrapped_q = textwrap.fill(
        q.text, width=WIDTH - 4,
        initial_indent="  ", subsequent_indent="    "
    )
    print(bold(wrapped_q))
    print()

    for opt in q.options:
        letter = opt["key"]
        text   = opt["text"]
        line   = f"{bold(letter)}) {text}"
        wrapped = textwrap.fill(
            line, width=WIDTH - 6,
            initial_indent="    ", subsequent_indent="       "
        )
        if q.user_answer and q.user_answer == letter:
            print(f"{C.BLUE}{wrapped}{C.RESET}  <--")
        else:
            print(wrapped)
    print()

    valid = q.option_keys + ["F", "S", "W", "Q"]
    keys_str = "|".join(q.option_keys)
    print(dim(f"  [{keys_str}] Answer  [F] Flag  [S] Skip  [W] Save & Quit  [Q] Quit without saving"))
    return valid


def show_answer_feedback(q: Question, user_ans: str):
    is_correct = user_ans == q.correct
    print()
    if is_correct:
        print(f"  {bold(green('CORRECT!'))}")
    else:
        print(f"  {bold(red('INCORRECT.'))}  "
              f"Correct answer: {bold(green(q.correct))} — "
              f"{bold(green(q.option_text(q.correct)))}")
    print()
    print(f"  {bold(cyan('Explanation:'))}")
    exp_wrapped = textwrap.fill(
        q.explanation, width=WIDTH - 4,
        initial_indent="  ", subsequent_indent="  "
    )
    print(dim(exp_wrapped))
    pause()


def run_exam(course: Course, questions: list[Question], start_elapsed: float = 0.0) -> float:
    total       = len(questions)
    unanswered  = [idx for idx, q in enumerate(questions) if q.user_answer is None]
    start_time  = time.time()
    i = 0

    while unanswered:
        if i >= len(unanswered):
            i = 0

        idx_in_list = unanswered[i]
        q = questions[idx_in_list]
        display_idx = idx_in_list + 1

        q_start = time.time()
        current_elapsed = start_elapsed + (time.time() - start_time)
        valid = display_question(q, display_idx, total, current_elapsed)
        ans   = prompt_choice(valid)
        q.time_spent += time.time() - q_start

        if ans == "Q":
            if get_yn("Really quit? Current run progress will be completely lost."):
                print(red("\n  Exam aborted.\n"))
                return -1.0
            continue

        if ans == "W":
            save_and_quit_exam(course, questions, current_elapsed)

        if ans == "S":
            i += 1
            continue

        if ans == "F":
            q.flagged = not q.flagged
            status = yellow("Flagged for review") if q.flagged else dim("Flag removed")
            print(f"\n  {status}")
            time.sleep(0.8)
            continue

        q.user_answer = ans
        unanswered.remove(idx_in_list)
        show_answer_feedback(q, ans)

    return start_elapsed + (time.time() - start_time)


# ─────────────────────────────────────────────
#  Results Screen & History Logging
# ─────────────────────────────────────────────
def results_screen(course: Course, questions: list[Question], total_time: float):
    clear()
    correct_qs = [q for q in questions if q.user_answer == q.correct]
    wrong_qs   = [q for q in questions if q.user_answer != q.correct]
    n     = len(questions)
    score = len(correct_qs)
    pct   = score / n * 100 if n else 0
    passed = score >= course.passing_score

    verdict = course.verdict(score)
    vcol    = course.verdict_color(score)

    print_header(f"  {course.short_title} — Results  ",
                 f"Total time: {fmt_time(total_time)}")

    print()
    print(center(bold(vcol(f"Score: {score}/{n}  ({pct:.1f}%)"))))
    print(center(vcol(verdict)))
    print()
    print(f"  {dim(f'Pass threshold: {course.passing_score}/{n} questions')}")
    print()
    print(rule())

    # ── Domain breakdown ──────────────────────────────────────────
    print(f"\n  {bold(yellow('Domain Breakdown:'))}")
    print()
    domains_in_set = list(dict.fromkeys(q.domain for q in questions))
    domain_results = {}
    for d in domains_in_set:
        d_qs      = [q for q in questions if q.domain == d]
        d_correct = [q for q in d_qs if q.user_answer == q.correct]
        d_pct     = len(d_correct) / len(d_qs) * 100 if d_qs else 0
        bar_len   = 20
        filled    = int(bar_len * d_pct / 100)
        bar       = "\u2588" * filled + "\u2591" * (bar_len - filled)
        col = green if d_pct >= 75 else (yellow if d_pct >= 50 else red)
        label = d.split("·")[1].strip() if "·" in d else d
        print(f"  {col(bar)}  {col(f'{d_pct:5.1f}%')}  "
              f"{bold(f'{len(d_correct)}/{len(d_qs)}')}  {dim(label)}")
        domain_results[d] = {"correct": len(d_correct), "total": len(d_qs)}

    print()
    print(rule())

    # Save to history file
    history = load_history()
    history.append({
        "course_id": course.id,
        "course_short_title": course.short_title,
        "score": score,
        "total_questions": n,
        "pct": pct,
        "passed": passed,
        "timestamp": datetime.now().isoformat(),
        "elapsed": total_time,
        "domain_results": domain_results
    })
    save_history(history)

    # ── Incorrect answers ─────────────────────────────────────────
    if wrong_qs:
        print(f"\n  {bold(red(f'Incorrect Answers ({len(wrong_qs)})'))}\n")
        for q in wrong_qs:
            given = q.option_text(q.user_answer) if q.user_answer else "—"
            corr  = q.option_text(q.correct)
            print(f"  {bold(cyan(f'Q{q.number}.'))} "
                  f"{textwrap.shorten(q.text, 60, placeholder='...')}")
            print(f"    {red(f'Your:    {q.user_answer}) {given}')}")
            print(f"    {green(f'Correct: {q.correct}) {corr}')}")
            print()
        print(rule())

    # ── Scoring guide ─────────────────────────────────────────────
    print(f"\n  {bold('Scoring Guide:')}")
    cols = [green, yellow, red]
    for i, tier in enumerate(course.scoring_guide):
        c = cols[min(i, len(cols) - 1)]
        print(f"  {c('*')} {tier['min']}+ correct: {tier['label']}")

    print()
    print(rule("=", C.CYAN + C.BOLD))

    print()
    if get_yn("Review all questions with explanations?"):
        review_all(questions)


def review_all(questions: list[Question]):
    for idx, q in enumerate(questions, start=1):
        clear()
        print_header(f"  Review: Q{idx}/{len(questions)}  ", q.domain)
        print()
        wrapped_q = textwrap.fill(
            q.text, width=WIDTH - 4,
            initial_indent="  ", subsequent_indent="    "
        )
        print(bold(wrapped_q))
        print()

        for opt in q.options:
            letter = opt["key"]
            text   = opt["text"]
            if letter == q.correct and letter == q.user_answer:
                marker = f"{green('[CORRECT]')} "
            elif letter == q.correct:
                marker = f"{green('[ANSWER] ')} "
            elif letter == q.user_answer:
                marker = f"{red('[YOURS]  ')} "
            else:
                marker = "           "
            line = f"{bold(letter)}) {text}"
            wrapped = textwrap.fill(
                marker + line, width=WIDTH - 2,
                initial_indent="  ", subsequent_indent="             "
            )
            print(wrapped)

        print()
        print(f"  {bold(cyan('Explanation:'))}")
        exp_wrapped = textwrap.fill(
            q.explanation, width=WIDTH - 4,
            initial_indent="  ", subsequent_indent="  "
        )
        print(dim(exp_wrapped))

        if idx < len(questions):
            pause("  Press Enter for next question...")
        else:
            pause("  Press Enter to finish...")


# ─────────────────────────────────────────────
#  Core Hub (Main Menu)
# ─────────────────────────────────────────────
def main_hub():
    while True:
        clear()
        print()
        print(rule("=", C.CYAN + C.BOLD))
        print(bold(cyan(center("Microsoft Certification Practice Exam Hub"))))
        print(dim(center("Practice engine with persistence, selector, and metrics")))
        print(rule("=", C.CYAN + C.BOLD))
        print()

        print(f"  {bold('1)')} Start a new exam")
        print(f"  {bold('2)')} Resume a saved exam")
        print(f"  {bold('3)')} View performance dashboard")
        print(f"  {bold('4)')} Import a practice course JSON")
        print(f"  {bold('5)')} Exit")
        print()

        choice = prompt_choice(["1", "2", "3", "4", "5"], "Select option (1-5): ")

        if choice == "1":
            clear()
            print_header("New Exam Session")
            course = select_course()
            config = mode_menu(course)
            questions = build_question_list(course, config)

            print()
            print(f"  {bold(cyan(f'Starting: {course.short_title}'))}")
            print(f"  {dim(f'{len(questions)} question(s) · pass mark {course.passing_score}/{len(course.questions)}')}")
            time.sleep(1)

            total_time = run_exam(course, questions)
            if total_time >= 0.0:
                results_screen(course, questions, total_time)

        elif choice == "2":
            resumed = resume_exam_picker()
            if resumed:
                course, questions, elapsed_time, save_name = resumed
                print(green(f"\n  Resuming {course.short_title} from saved point..."))
                time.sleep(1)
                total_time = run_exam(course, questions, start_elapsed=elapsed_time)
                if total_time >= 0.0:
                    results_screen(course, questions, total_time)
                    # Clean up the state after finishing successfully
                    delete_exam_state(save_name)

        elif choice == "3":
            performance_dashboard_menu()

        elif choice == "4":
            import_course_menu()

        elif choice == "5":
            print(cyan("\n  Happy learning! Exiting exam hub...\n"))
            break


if __name__ == "__main__":
    main_hub()
