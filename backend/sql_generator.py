import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema_reader import get_schema_text

load_dotenv()

client = genai.Client(api_key=os.getenv("AI_API_KEY"))

SYSTEM_PROMPT = """You are a PostgreSQL expert.
You will be given a database schema and a question.
Rules:
- Return ONLY one SQL query. No explanation, no markdown.
- Only write SELECT statements.
- Use only the tables and columns listed in the schema.
- If the question cannot be answered from the schema, return exactly: CANNOT_ANSWER
"""


def clean_sql(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("sql"):
            text = text[3:]
    return text.strip()


def generate_sql(question):
    schema = get_schema_text()
    prompt = f"Database schema:\n{schema}\n\nQuestion: {question}"

    response = client.models.generate_content(
        model=os.getenv("AI_MODEL"),
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return clean_sql(response.text)

