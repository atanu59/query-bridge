import time
from sql_generator import generate_sql
from validator import validate_sql
from executor import run_query


def elapsed_ms(since):
    return round((time.perf_counter() - since) * 1000)


def answer_question(question):
    start = time.perf_counter()
    timings = {}

    def finish(result):
        timings["total_ms"] = elapsed_ms(start)
        result["timings"] = timings
        return result

    try:
        t = time.perf_counter()
        raw_sql = generate_sql(question)
        timings["ai_ms"] = elapsed_ms(t)
    except Exception as e:
        return finish({"ok": False, "error": f"AI request failed: {e}"})

    is_valid, result = validate_sql(raw_sql)
    if not is_valid:
        return finish({"ok": False, "error": result, "sql": raw_sql})

    try:
        t = time.perf_counter()
        data = run_query(result)
        timings["db_ms"] = elapsed_ms(t)
    except Exception as e:
        return finish({"ok": False, "error": f"Query failed: {e}", "sql": result})

    return finish({"ok": True, "sql": result, **data})

