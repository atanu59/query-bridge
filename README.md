# Query Bridge

Ask your database questions in plain English. Query Bridge turns a question into SQL using an AI model, checks that the SQL is safe, runs it, and shows the results in a table, along with the SQL it generated and how long each step took.

![Query Bridge demo](docs/images/demo.png)

## How it works

1. You type a question in the React interface.
2. The Flask API reads the database schema (tables, columns, foreign keys) and sends it, together with your question, to the AI model.
3. The model returns a SQL query.
4. The query is validated: a single `SELECT` statement only, with write and admin keywords blocked.
5. It runs in a read-only session with a timeout and a row limit.
6. The results come back as a table, with the generated SQL and timing for the AI and database steps.

## Tech stack

| Layer    | Technology                                      |
| -------- | ----------------------------------------------- |
| Frontend | React (Vite)                                    |
| Backend  | Python, Flask                                   |
| Database | PostgreSQL                                      |
| AI       | Google Gemini API (model name set in `.env`)    |

## Project structure

```
query-bridge/
├── backend/
│   ├── app.py            # Flask API (routes)
│   ├── pipeline.py       # question -> SQL -> validate -> run -> result (with timings)
│   ├── sql_generator.py  # builds the prompt and calls the AI model
│   ├── validator.py      # checks the generated SQL is a safe SELECT
│   ├── executor.py       # runs the query with timeout, read-only session and row limit
│   ├── schema_reader.py  # reads the database schema into text for the prompt
│   ├── db_config.py      # the single place that creates database connections
│   ├── requirements.txt
│   └── .env.example      # template for your own .env
├── frontend/             # React app
├── docs/
│   ├── sample_data.sql   # sample shop database
│   └── images/
├── .gitignore
└── README.md
```

## Safety measures

- Only a single `SELECT` (or `WITH ... SELECT`) statement is allowed.
- Write and admin keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, and so on) are rejected.
- Queries run in a read-only database session.
- Each query has a 5-second timeout.
- Results are capped at 100 rows.
- Secrets live in `.env`, which is excluded from Git.

These checks are a first line of defence for local development. For a database that holds real data, also connect with a dedicated read-only database user (see [Limitations](#limitations)).

## Getting started

### Prerequisites

- Python 3.10 or newer
- Node.js (current LTS)
- PostgreSQL, with the `psql` command available
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)

### 1. Clone the repository

```
git clone https://github.com/atanu59/query-bridge.git
cd query-bridge
```

### 2. Create the sample database

```
psql -U postgres -c "CREATE DATABASE shop_db;"
psql -U postgres -d shop_db -f docs/sample_data.sql
```

This creates four tables (`customers`, `orders`, `products`, `order_items`) with a small amount of sample data. To use your own database instead, skip this step and point the `DB_*` values in `.env` at it.

### 3. Set up the backend

```
cd backend
python -m venv venv
```

Activate the virtual environment:

- Windows (Command Prompt): `venv\Scripts\activate`
- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- macOS / Linux: `source venv/bin/activate`

Then install the packages and create your settings file:

```
pip install -r requirements.txt
```

Copy `.env.example` to `.env` (Windows: `copy .env.example .env`, macOS / Linux: `cp .env.example .env`) and fill in your own values. Never commit `.env`.

Start the API:

```
python app.py
```

Check it at <http://127.0.0.1:5000/api/health>. You should see `{"status": "ok"}`.

### 4. Set up the frontend

In a second terminal:

```
cd frontend
npm install
npm run dev
```

Open the address Vite prints, usually <http://localhost:5173>.

## Example questions

Try these on the sample database:

- Which customers placed orders over 500?
- What is the total amount spent by each customer?
- Which customers have never placed an order?
- How many units of each product have been sold?
- Show orders placed after 15 October 2026, newest first.

## API

### `GET /api/health`

Returns `{"status": "ok"}`.

### `POST /api/query`

Request body:

```json
{ "question": "Which customers placed orders over 500?" }
```

Successful response:

```json
{
  "ok": true,
  "sql": "SELECT ...",
  "columns": ["customer_id", "name"],
  "rows": [[3, "Sam"], [1, "Amit"]],
  "row_count": 2,
  "timings": { "ai_ms": 1950, "db_ms": 8, "total_ms": 1962 }
}
```

If something fails, `ok` is `false` and `error` explains why. The `sql` field is included when a query was generated, so you can see what the model wrote.

## Limitations

- The model can still write incorrect SQL. Always read the generated SQL before trusting a result.
- The free Gemini tier has rate limits and can return temporary "model overloaded" (503) errors. Wait a few seconds and run the question again.
- On the free tier, the content you send can be used by Google to improve its products. Don't connect a database containing private or sensitive data while using a free key.
- The keyword check in the validator is deliberately simple and can reject harmless queries that contain a blocked word.
- Flask runs in debug mode for development. Don't deploy it as it is.
- Switching to another database engine (for example MySQL) would need changes to the driver, the schema queries, and the prompt, though connection setup now lives in `db_config.py`.

## Roadmap

- [x] Phase 1: single-database text-to-SQL with a React interface and timing display
- [ ] Phase 1: accuracy test set and automatic retry when the generated SQL fails
- [ ] Phase 2: multiple databases, with a metadata database that stores schema information and descriptions
- [ ] Phase 3: authentication (user and admin) and a query history page

## About

This project started as a team internship project. I rebuilt it from scratch to understand how every part works, from schema reading and prompt design to validation, execution, and the React interface.
