from django.db import connection


def safe_raw_query(query: str, params: tuple = ()):  # parameterized query
    """Execute a raw SQL query safely using parameterized inputs.

    Example:
        rows = safe_raw_query('SELECT id, username FROM accounts_user WHERE username = %s', (username,))
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0]
                   for col in cursor.description] if cursor.description else []
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
