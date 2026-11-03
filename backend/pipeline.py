from sql_generator import generate_sql
from validator import validate_sql
from executor import run_query


def answer_question(question):
    try:
        raw_sql = generate_sql(question)
    except Exception as e:
        return {"ok": False, "error": f"AI request failed: {e}"}
    is_valid, result = validate_sql(raw_sql)
    if not is_valid:
        return {"ok": False, "error": result, "sql": raw_sql}
    try:
        data = run_query(result)
    except Exception as e:
        return {"ok": False, "error": f"Query failed: {e}", "sql": result}

    return {"ok": True, "sql": result, **data}


