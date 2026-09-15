"""
=============================================================================
Minor Project 1: AI-Powered Resume Screening & ATS Optimizer
File: db_manager.py
Author: B.Tech 3rd Year AI & ML Project
Description: SQLite database storage for audit trail and evaluation history.
=============================================================================
"""

import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "ats_history.db"


def init_db():
    """
    Creates the SQLite database table for evaluation history if it does not exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            jd_title TEXT,
            ats_score REAL,
            semantic_score REAL,
            skill_score REAL,
            match_grade TEXT,
            missing_skills TEXT,
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_evaluation(candidate_name: str, jd_title: str, results: dict):
    """
    Saves an evaluation record to the SQLite database.
    """
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    missing_str = ", ".join(results["skill_analysis"].get("missing_skills", []))

    cursor.execute("""
        INSERT INTO evaluations 
        (candidate_name, jd_title, ats_score, semantic_score, skill_score, match_grade, missing_skills, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        jd_title,
        results["final_ats_score"],
        results["semantic_similarity_pct"],
        results["skill_coverage_pct"],
        results["match_grade"],
        missing_str,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_evaluation_history() -> pd.DataFrame:
    """
    Retrieves evaluation history as a Pandas DataFrame for dashboard rendering.
    """
    init_db()
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM evaluations ORDER BY created_at DESC", conn)
    conn.close()
    return df


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
