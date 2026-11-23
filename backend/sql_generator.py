from schema_reader import get_schema_text
from cloud_model import ask_cloud
from local_model import ask_local

SYSTEM_PROMPT = """You are a PostgreSQL expert.
You will be given a database schema and a question.
Rules:
- Return ONLY one SQL query. No explanation, no markdown.
- Only write SELECT statements.
- Use only the tables and columns listed in the schema.
- If the question cannot be answered from the schema, return exactly: CANNOT_ANSWER
"""


def clean_sql(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("sql"):
            text = text[3:]
    return text.strip()


def generate_sql(question):
    schema = get_schema_text()
    prompt = f"Database schema:\n{schema}\n\nQuestion: {question}"

    try:
        text = ask_cloud(prompt, SYSTEM_PROMPT)
        print("[AI] answered by: cloud")
    except Exception as cloud_error:
        print(f"[AI] cloud failed ({cloud_error}), trying local model")
        try:
            text = ask_local(prompt, SYSTEM_PROMPT)
            print("[AI] answered by: local")
        except Exception as local_error:
            print(f"[AI] local failed: {local_error}")
            raise RuntimeError(
                "No AI model is available right now. Check your internet "
                "connection and that Ollama is running, then try again."
            ) from local_error

    return clean_sql(text)