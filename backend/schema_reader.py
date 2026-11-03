from db_config import get_connection

def get_schema_text():
    conn = get_connection()
    cur = conn.cursor()

    # 1. All columns of all tables in the public schema
    cur.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    columns = cur.fetchall()

    # 2. Foreign key relationships
    cur.execute("""
        SELECT
            tc.table_name, kcu.column_name,
            ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage ccu
            ON tc.constraint_name = ccu.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = 'public';
    """)
    foreign_keys = cur.fetchall()

    cur.close()
    conn.close()

    # 3. Build a readable text description
    tables = {}
    for table, column, dtype in columns:
        tables.setdefault(table, []).append(f"{column} ({dtype})")

    lines = []
    for table, cols in tables.items():
        lines.append(f"Table {table}: " + ", ".join(cols))

    for table, column, f_table, f_column in foreign_keys:
        lines.append(f"{table}.{column} references {f_table}.{f_column}")

    return "\n".join(lines)
