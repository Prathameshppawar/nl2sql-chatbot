# 🧠 NL2SQL API

Convert natural language questions into SQL queries and run them against a real database using Groq, HuggingFace embeddings, and ChromaDB.

## 🧪 Features

- 🧾 Converts plain English into SQL queries using **Groq (Llama-3)**
- 🧠 Understands database schema using **ChromaDB + HuggingFace embeddings**
- 💾 Runs queries on a live **SQLite database**
- ✅ Validates SQL before execution
- 🪵 Logs every query and result using Loguru
- 🐳 Fully containerized with Docker + Compose
- 📊 Includes `/stats` endpoint for database insights
- 📚 Auto-generated interactive docs at `/docs` (Swagger)

## 📦 Tech Stack

| Layer        | Tech                                |
|--------------|--------------------------------------|
| LLM          | Groq (Mixtral-8x7b)                  |
| Embeddings   | HuggingFace (`llama-3.1-8b-instant`)     |
| Vector DB    | ChromaDB                             |
| API          | FastAPI + uvicorn                    |
| DB           | SQLite                               |
| Logging      | Loguru                               |
| Dev Tooling  | uv + Docker + Compose                |

---

## 🚀 Running Locally

### Clone and setup env

```bash
git clone https://github.com/Prathameshppawar/nl2sql-chatbot.git
cd nl2sql-chatbot
cp .env.example .env  # Add your GROQ_API_KEY

```
### Run using `uv`

```bash
uv venv && source .venv/bin/activate
uv sync
uvicorn main:app --reload
```
Or:

### Run with 🐋Docker

```bash 
docker-compose up --build
```

Visit: http://localhost:8000/docs


## 🗃️ Database Schema Overview

The current database simulates a real-world **food delivery system**, containing entities like:

| Table Name       | Description                                  |
|------------------|----------------------------------------------|
| `users`          | Stores user/customer profiles                |
| `restaurants`    | Basic details about restaurants              |
| `menu_items`     | Menu items offered by restaurants            |
| `orders`         | Orders placed by users                       |
| `order_items`    | Individual items in each order               |
| `delivery_agents`| Info about delivery personnel                |

This schema allows natural language queries such as:

- "List all orders with customer names and dish names"
- "Show all items ordered by Bob last week"
- "What is the most popular dish?"
- "Which delivery agent handled the most orders?"
- "Total revenue per restaurant in June"

The schema is embedded into the vector database (Chroma) using HuggingFace embeddings and retrieved as context for the LLM.

> 📁 File: `data/schema.txt` contains a textual description of this schema used for grounding.

### ✅ Example Query

`POST /query`
```json
{
  "question": "List all orders with customer names and dish names"
}

```

#### Response: 
```json
{
  "sql": "SELECT u.name AS customer_name, m.name AS dish_name, o.order_date \nFROM orders o \nJOIN users u ON o.user_id = u.id \nJOIN menu_items m ON o.restaurant_id = m.restaurant_id",
  "result": [
    {
      "customer_name": "Alice",
      "dish_name": "Margherita Pizza",
      "order_date": "2024-07-01"
    },
    {
      "customer_name": "Bob",
      "dish_name": "Butter Chicken",
      "order_date": "2024-07-02"
    }
  ]
}

```

### 📊 Stats Endpoint
`GET /stats`
Returns DB-level insights like user count, total revenue, recent orders.

```json
{
  "users_count": 2,
  "orders_count": 2,
  "restaurants_count": 2,
  "menu_items_count": 2,
  "order_items_count": 2,
  "delivery_agents_count": 2,
  "most_recent_order": "2024-07-02",
  "total_revenue": 970
}
```

### 🪵 Logging

- All questions, SQLs, and results are saved to logs/nl2sql.log

- Automatic rotation (1 MB), retention (7 days)

### 🧪 Testing
Visit the interactive Swagger UI:
http://localhost:8000/docs

Or use curl:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What dishes did Bob order?"}'
```
### 🧱 Project Structure
```pgsql

.
├── main.py
├── agent/
│   └── langchain_agent.py
├── utils/
│   ├── query_executor.py
│   └── logger.py
├── data/
│   └── schema.txt
├── db/
│   └── sample.db
├── logs/
│   └── nl2sql.log
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

## 📝 Notes & Limitations
> ⚠️ This is a pre-release version and under active development.

- 🚫 Offline Only: The API is currently available only on local environments (localhost). No cloud deployment has been done yet.

- 🛠️ Manual DB Seeding: The SQLite database (db/sample.db) is pre-populated manually. No automatic migration or seeding logic is included yet.

- 🧠 Schema Grounding Only: NL2SQL understanding is based on vector retrieval from schema descriptions (no fine-tuning).

- 💬 No Authentication: This project currently runs without user authentication or rate-limiting.

- 🔐 No Data Persistence for Logs: Logs are saved to local file (logs/nl2sql.log) only. No external logging system (e.g., ELK, Prometheus) is connected.

- 🧪 Not Production-Hardened: No async DB pooling, retry policies, or circuit breakers are implemented.

- 📦 Docker Used for Local Packaging Only: While Docker/Compose are set up, images are not pushed to any registry (e.g., DockerHub).


## 👨‍💻 Author
Made with 💻 + ☕ by [Prathamesh Pawar](https://github.com/Prathameshppawar)