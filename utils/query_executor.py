import sqlite3
from typing import List, Dict
from loguru import logger

DB_PATH = "db/sample.db"

def is_valid_sql(sql: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(f"EXPLAIN {sql}")
        conn.close()
        return True
    except sqlite3.Error as e:
        logger.error(f"SQL validation failed: {e}")
        return False

def execute_query(sql: str) -> List[Dict]:
    if not is_valid_sql(sql):
        return [{"error": "Invalid SQL syntax"}]

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return [{"error": str(e)}]
