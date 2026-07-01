# HR Attendance & Performance Bot

A conversational assistant that lets HR staff query employee attendance records and get automatic performance evaluations, built with **LangGraph**, **LangChain**, **Groq (OpenAI OSS 120B)**, and **PostgreSQL (Supabase)**.

---

## Features

- Look up an employee by full or partial name
- Retrieve monthly or yearly attendance (Present / Absent / Late / Leave counts)
- Count total absences and total late marks
- Calculate yearly attendance percentage
- Evaluate employee performance against company policy
- Handles ambiguous name matches and "not found" cases gracefully
- Simple CLI chat loop for interacting with the bot

## Performance Policy

| Attendance % | Rating            |
| ------------ | ----------------- |
| ≥ 90%        | Excellent         |
| 80% – 89%    | Good              |
| 60% – 79%    | Needs Improvement |
| < 60%        | Poor              |

## Architecture

```
User (CLI) → app.py → agent.py (LangGraph StateGraph)
                          │
                          ├── chatbot node → llm.py (ChatGroq + system prompt)
                          └── tools node   → tools.py → queries.py → database.py → PostgreSQL
```

- **app.py** — command-line chat loop; keeps conversation history and calls the compiled graph.
- **agent.py** — defines the LangGraph state machine: a `chatbot` node (LLM call) and a `tools` node (tool execution), wired together with `tools_condition` so the LLM can call tools and receive results in a loop.
- **llm.py** — configures the Groq-backed LLM and holds the system prompt describing the assistant's role and policy.
- **tools.py** — LangChain `@tool`-decorated functions exposed to the LLM (employee lookup, attendance queries, performance evaluation). Each tool resolves the employee name first and handles "not found" / "ambiguous" cases before querying data.
- **queries.py** — raw parameterized SQL against the `attendence` table.
- **database.py** — SQLAlchemy engine/connection setup, reads `DATABASE_URL` from `.env`.
- **performance.py** — pure function mapping an attendance percentage to a rating + remark.
- **attendance.csv** — sample/seed data (columns: `attendance_id, employee_id, employee_name, date, status`).

## Requirements

- Python 3.14 (see `.python-version`)
- A PostgreSQL database (e.g. Supabase) with an `attendence` table matching the schema below
- A Groq API key

### Database schema (`attendence` table)

| Column        | Type                                           |
| ------------- | ---------------------------------------------- |
| attendance_id | integer                                        |
| employee_id   | text                                           |
| employee_name | text                                           |
| date          | date                                           |
| status        | text (`Present` / `Absent` / `Late` / `Leave`) |

## Setup

1. **Clone the repo and create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install langgraph langchain langchain-core langchain-groq sqlalchemy psycopg2-binary python-dotenv pandas
   ```
   > Note: the current `requirements.txt` is inaccurate — see the QA notes below.

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Never commit this file. Confirm `.env` is listed in `.gitignore`.

4. **Load sample data (optional)**

   Import `attendance.csv` into the `attendence` table using your preferred method (e.g. `psql \copy`, a Python/pandas script, or Supabase's table import UI).

5. **Test the database connection**
   ```bash
   python database.py
   ```

6. **Run the bot**
   ```bash
   python app.py
   ```
   Type your question at the `You :` prompt, e.g.:
   ```
   You : What is Ali Ahmed's attendance percentage for 2023?
   You : Evaluate Ali Ahmed's performance for 2023
   ```
   Type `exit` to quit.

## Project Structure

```
.
├── agent.py            # LangGraph graph definition
├── app.py               # CLI entry point
├── database.py          # DB engine/connection helpers
├── llm.py                # LLM config + system prompt
├── performance.py       # Performance rating logic
├── queries.py            # SQL queries
├── tools.py               # LangChain tool wrappers
├── attendance.csv        # Sample attendance data
├── requirements.txt
├── pyproject.toml
└── .env                  # Not committed — holds secrets
```

## Known Limitations

- CLI-only; no web or API interface yet.
- No automated tests.
- No input validation on month/year values passed to tools.
- Attendance percentage calculation only accounts for "Present" days over total logged days (Leave days are not excluded from the denominator).

## License

Add a license of your choice.