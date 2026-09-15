"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: test_suite.py
Author: B.Tech 3rd Year AI & ML Project
Description: Automated unit testing suite for verification.
=============================================================================
"""

import unittest
import os
from resume_parser import clean_text, extract_contact_info
from skill_extractor import extract_skills_by_category, compare_skills
from ats_matcher import compute_ats_score
from db_manager import init_db, save_evaluation, get_evaluation_history


class TestATSProject(unittest.TestCase):

    def test_clean_text(self):
        dirty = "  Hello \n\n World!  • Bullet "
        cleaned = clean_text(dirty)
        self.assertEqual(cleaned, "Hello World! Bullet")

    def test_extract_contact_info(self):
        sample = "Email: test.user@gmail.com | Phone: 9876543210 | github.com/testuser"
        info = extract_contact_info(sample)
        self.assertEqual(info["email"], "test.user@gmail.com")
        self.assertEqual(info["github"], "https://github.com/testuser")

    def test_skill_extractor(self):
        sample_text = "Proficient in Python, TensorFlow, SQL, Docker, and Git."
        skills = extract_skills_by_category(sample_text)
        self.assertIn("Python", skills["Programming Languages"])
        self.assertIn("Tensorflow", skills["Machine Learning & AI"])

    def test_ats_matcher_bounds(self):
        res = "Python machine learning data science"
        jd = "Looking for Python machine learning engineer"
        scores = compute_ats_score(res, jd)
        self.assertGreaterEqual(scores["final_ats_score"], 0.0)
        self.assertLessEqual(scores["final_ats_score"], 100.0)

    def test_database(self):
        init_db()
        dummy_res = compute_ats_score("Python developer", "Python developer required")
        save_evaluation("Unit Test Candidate", "Unit Test JD", dummy_res)
        df = get_evaluation_history()
        self.assertFalse(df.empty)


if __name__ == "__main__":
    unittest.main()
