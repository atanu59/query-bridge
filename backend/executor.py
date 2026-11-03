from db_config import get_connection

MAX_ROWS = 100


def run_query(sql):
    conn = get_connection()
    conn.set_session(readonly=True)
    try:
        cur = conn.cursor()
        cur.execute("SET statement_timeout = 5000")
        cur.execute(f"SELECT * FROM ({sql}) AS limited_query LIMIT {MAX_ROWS}")
        columns = [col[0] for col in cur.description]
        raw_rows = cur.fetchall()
        rows = [
            [v if v is None or isinstance(v, (int, float, str, bool)) else str(v) for v in row]
            for row in raw_rows
        ]
        return {"columns": columns, "rows": rows, "row_count": len(rows)}
    finally:
        conn.close()


if __name__ == "__main__":
    print(run_query("SELECT * FROM customers"))
