"""
Headless Verification Script for AI Resume ATS Optimizer
"""

import sys
import os

print("--- Running Full System Verification ---")

# 1. Test resume_parser
from resume_parser import parse_resume_file, extract_contact_info, clean_text
sample_raw = "Email: john@domain.com | Phone: 1234567890 | github.com/johndoe\nSkills: Python, PyTorch, SQL."
contacts = extract_contact_info(sample_raw)
assert contacts["email"] == "john@domain.com"
assert contacts["github"] == "https://github.com/johndoe"
print("[OK] Module 1 (resume_parser.py): PASS")

# 2. Test skill_extractor
from skill_extractor import extract_skills_by_category, compare_skills
skills = extract_skills_by_category("Python TensorFlow PyTorch SQL Docker")
assert "Python" in skills["Programming Languages"]
comparison = compare_skills("Python PyTorch Docker", "Python PyTorch Kubernetes AWS")
assert comparison["skill_coverage_pct"] > 0
print("[OK] Module 2 (skill_extractor.py): PASS")

# 3. Test ats_matcher
from ats_matcher import compute_ats_score
match_res = compute_ats_score("Python ML Engineer PyTorch", "Looking for Python ML Engineer PyTorch")
assert match_res["final_ats_score"] > 50.0
print("[OK] Module 3 (ats_matcher.py): PASS")

# 4. Test recommendation_engine
from recommendation_engine import generate_recommendations
recs = generate_recommendations(match_res, "Short resume text", contacts)
assert "summary_advice" in recs
print("[OK] Module 4 (recommendation_engine.py): PASS")

# 5. Test db_manager
from db_manager import init_db, save_evaluation, get_evaluation_history, clear_evaluation_history
init_db()
save_evaluation("Headless Test Candidate", "ML Role", match_res)
df = get_evaluation_history()
assert not df.empty
clear_evaluation_history()
df_cleared = get_evaluation_history()
assert df_cleared.empty
print("[OK] Module 5 (db_manager.py with clear_evaluation_history): PASS")

# 6. Test api.py import
import api
print("[OK] Module 6 (api.py): PASS")

print("\nSUCCESS: ALL 6 SYSTEM MODULES PASSED VERIFICATION PERFECTLY!")
