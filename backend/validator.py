import re

FORBIDDEN_WORDS = [
    "insert", "update", "delete", "drop", "alter", "truncate",
    "create", "grant", "revoke", "copy", "execute", "call",
]


def validate_sql(sql):
    """Returns (True, clean_sql) if safe, or (False, reason) if not."""

    if sql.strip() == "CANNOT_ANSWER":
        return False, "This question can't be answered from the database."

    cleaned = sql.strip().rstrip(";").strip()

    if ";" in cleaned:
        return False, "Only one SQL statement is allowed."

    lowered = cleaned.lower()

    if not (lowered.startswith("select") or lowered.startswith("with")):
        return False, "Only SELECT queries are allowed."

    for word in FORBIDDEN_WORDS:
        if re.search(rf"\b{word}\b", lowered):
            return False, f"Forbidden keyword found: {word}"

    return True, cleaned


if __name__ == "__main__":
    tests = [
        "SELECT * FROM customers;",
        "DELETE FROM customers;",
        "SELECT * FROM customers; DROP TABLE orders;",
        "WITH x AS (DELETE FROM orders RETURNING *) SELECT * FROM x",
        "CANNOT_ANSWER",
    ]
    for t in tests:
        print(t, "->", validate_sql(t))