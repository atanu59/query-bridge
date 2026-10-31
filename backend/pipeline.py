from sql_generator import generate_sql
from validator import validate_sql
from executor import run_query


def answer_question(question):
    # 1. Ask the AI for SQL
    try:
        raw_sql = generate_sql(question)
    except Exception as e:
        return {"ok": False, "error": f"AI request failed: {e}"}

    # 2. Check the SQL is safe
    is_valid, result = validate_sql(raw_sql)
    if not is_valid:
        return {"ok": False, "error": result, "sql": raw_sql}

    # 3. Run it on the database
    try:
        data = run_query(result)
    except Exception as e:
        return {"ok": False, "error": f"Query failed: {e}", "sql": result}

    return {"ok": True, "sql": result, **data}


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type quit): ")
        if question.strip().lower() == "quit":
            break
        print(answer_question(question))