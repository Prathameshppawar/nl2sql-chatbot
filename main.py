from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.langchain_agent import generate_sql_query
from utils.query_executor import execute_query
import os
from utils.logger import logger

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def get_sql_and_results(req: QueryRequest):
    try:
        # Generate SQL from NL
        sql = generate_sql_query(req.question)
        print("Generated SQL:\n", sql)

        # Execute SQL on database
        result = execute_query(sql)

        logger.info(f"User question: {req.question}")
        logger.info(f"Generated SQL: {sql}")
        logger.info(f"Result: {result}")

        return {
            "sql": sql,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats():
    import sqlite3
    from datetime import datetime

    DB_PATH = "db/sample.db"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    stats = {}

    # Basic table row counts
    for table in ["users", "orders", "restaurants", "menu_items", "order_items", "delivery_agents"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[f"{table}_count"] = cursor.fetchone()[0]

    # Most recent order
    cursor.execute("SELECT MAX(order_date) FROM orders")
    stats["most_recent_order"] = cursor.fetchone()[0]

    # Total revenue
    cursor.execute("SELECT SUM(total_amount) FROM orders")
    stats["total_revenue"] = cursor.fetchone()[0]

    conn.close()

    return stats
