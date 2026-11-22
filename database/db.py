"""
database/db.py - SQLite Persistence Layer for Quantum Experiment History
Provides safe saving, querying, clearing, and CSV export for laboratory runs.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd

DB_FILE = os.path.join(os.path.dirname(__file__), "quantum_lab.db")


def get_db_connection() -> Optional[sqlite3.Connection]:
    """Safely opens an SQLite connection."""
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def init_db() -> bool:
    """Initializes the SQLite database table schema if it does not exist."""
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS experiment_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    experiment_type TEXT NOT NULL,
                    num_qubits INTEGER NOT NULL,
                    num_shots INTEGER NOT NULL,
                    counts_json TEXT NOT NULL,
                    summary TEXT
                )
            """)
        return True
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return False
    finally:
        conn.close()


def save_experiment(
    experiment_type: str,
    num_qubits: int,
    num_shots: int,
    counts: Dict[str, int],
    summary: str = "",
) -> Optional[int]:
    """
    Saves an experiment run to SQLite. Never raises an uncaught exception.
    """
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        counts_str = json.dumps(counts)
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO experiment_history (timestamp, experiment_type, num_qubits, num_shots, counts_json, summary)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (now_str, experiment_type, num_qubits, num_shots, counts_str, summary),
            )
            return cursor.lastrowid
    except Exception as e:
        print(f"Failed to save experiment: {e}")
        return None
    finally:
        conn.close()


def get_all_experiments(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves previous experiments ordered by most recent."""
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cursor = conn.execute(
            """
            SELECT id, timestamp, experiment_type, num_qubits, num_shots, counts_json, summary
            FROM experiment_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "experiment_type": row["experiment_type"],
                "num_qubits": row["num_qubits"],
                "num_shots": row["num_shots"],
                "counts": json.loads(row["counts_json"]),
                "summary": row["summary"],
            })
        return results
    except Exception as e:
        print(f"Failed to fetch experiment history: {e}")
        return []
    finally:
        conn.close()


def clear_history() -> bool:
    """Clears all records from experiment history."""
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn:
            conn.execute("DELETE FROM experiment_history")
        return True
    except Exception as e:
        print(f"Failed to clear history: {e}")
        return False
    finally:
        conn.close()


def export_history_to_df() -> pd.DataFrame:
    """Exports history to a pandas DataFrame for CSV download."""
    records = get_all_experiments(limit=500)
    if not records:
        return pd.DataFrame(columns=["id", "timestamp", "experiment_type", "num_qubits", "num_shots", "counts", "summary"])

    rows = []
    for r in records:
        rows.append({
            "Experiment ID": r["id"],
            "Timestamp": r["timestamp"],
            "Experiment Type": r["experiment_type"],
            "Qubits": r["num_qubits"],
            "Shots": r["num_shots"],
            "Measurement Counts": str(r["counts"]),
            "Summary": r["summary"],
        })
    return pd.DataFrame(rows)
