from app.database import get_connection


# =========================================
# REGISTER
# =========================================

def register(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    if user is not None:

        connection.close()

        return {
            "error": "Username already exists"
        }

    cursor.execute(
        """
        INSERT INTO users
        (username, password)
        VALUES (?, ?)
        """,
        (username, password)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Registration successful"
    }


# =========================================
# LOGIN
# =========================================

def login(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:

        return None

    return {
        "id": user["id"],
        "username": user["username"]
    }