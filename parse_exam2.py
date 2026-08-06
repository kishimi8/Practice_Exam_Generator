import re
import json
from pathlib import Path

# Paths
markdown_file = Path("/Users/ibrahimkishimi/Downloads/DP-600_Practice_Exam_2.md")
output_json = Path("/Users/ibrahimkishimi/.gemini/antigravity-ide/scratch/dp600-exam/courses/dp600_exam2.json")

# Domain names mapped to questions
DOMAIN1 = "Domain 1 · Plan, Implement & Manage"
DOMAIN2 = "Domain 2 · Prepare and Serve Data"
DOMAIN3 = "Domain 3 · Implement & Manage Semantic Models"
DOMAIN4 = "Domain 4 · Explore and Analyze Data"

def get_domain_for_q(num):
    if 1 <= num <= 8:
        return DOMAIN1
    elif 9 <= num <= 28:
        return DOMAIN2
    elif 29 <= num <= 41:
        return DOMAIN3
    elif 42 <= num <= 50:
        return DOMAIN4
    return "General"

def parse_exam():
    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content into questions block and answer key block
    parts = re.split(r"## Answer Key with Explanations", content, flags=re.IGNORECASE)
    if len(parts) < 2:
        print("Could not find Answer Key section.")
        return
    
    q_section = parts[0]
    ans_section = parts[1]

    # 1. Parse answers and explanations
    answers = {}      # {q_num: (correct_letter, explanation)}
    # Find patterns like: **1. B** — capacity metrics...
    # Or: **10. A** — the SQL...
    ans_matches = re.finditer(
        r"\*\*(\d+)\.\s*([A-E])\*\*\s*[\u2014-]\s*(.*?)(?=\n\n\*\*|\n\n---|\Z)", 
        ans_section, 
        re.DOTALL
    )
    for m in ans_matches:
        q_num = int(m.group(1))
        ans_letter = m.group(2)
        exp_text = m.group(3).strip().replace("\n", " ")
        # Clean double spaces
        exp_text = re.sub(r"\s+", " ", exp_text)
        answers[q_num] = (ans_letter, exp_text)

    # 2. Parse questions
    # Questions start with **1.**, **2.** up to **50.**
    questions_data = []
    
    # Split the q_section by question headers
    q_blocks = re.split(r"\n\*\*(\d+)\.\*\*\s*", q_section)
    # The first element in q_blocks is header text before question 1.
    # The subsequent elements come in pairs: [number, text + options]
    
    for i in range(1, len(q_blocks), 2):
        q_num = int(q_blocks[i])
        block_content = q_blocks[i+1]
        
        # Split block content into question text and options
        # Options are lines starting with A), B), C), D), E)
        lines = block_content.strip().split("\n")
        q_text_lines = []
        options_list = []
        
        for line in lines:
            line_str = line.strip()
            opt_match = re.match(r"^([A-E])\)\s*(.*)", line_str)
            if opt_match:
                options_list.append({
                    "key": opt_match.group(1),
                    "text": opt_match.group(2).strip()
                })
            else:
                if line_str:
                    q_text_lines.append(line_str)
                    
        q_text = " ".join(q_text_lines).strip()
        q_text = re.sub(r"\s+", " ", q_text)
        
        correct, explanation = answers.get(q_num, ("A", "Explanation placeholder"))
        
        questions_data.append({
            "number": q_num,
            "domain": get_domain_for_q(q_num),
            "text": q_text,
            "options": options_list,
            "correct": correct,
            "explanation": explanation
        })

    # Prepare final course dictionary structure
    course_data = {
        "id": "dp600_exam2",
        "title": "DP-600: Implementing Analytics Solutions Using Microsoft Fabric — Practice Exam #2",
        "short_title": "DP-600 · Practice Exam #2",
        "passing_score": 45,
        "description": "50 fresh, distinct questions targeting DP-600 core objectives.",
        "domains": [DOMAIN1, DOMAIN2, DOMAIN3, DOMAIN4],
        "scoring_guide": [
            { "min": 45, "label": "EXCELLENT — Likely exam-ready!" },
            { "min": 38, "label": "GOOD — Review missed domains and practice more." },
            { "min": 0,  "label": "NEEDS WORK — More hands-on practice recommended." }
        ],
        "questions": questions_data
    }

    # Save to JSON
    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(course_data, out, indent=2)
    print(f"Created course JSON file with {len(questions_data)} questions at: {output_json}")

if __name__ == "__main__":
    parse_exam()
