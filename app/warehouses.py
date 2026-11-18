from app.database import get_connection


def create_warehouse(name, location):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO warehouses
            (
                name,
                location
            )
            VALUES (?, ?)
            """,
            (
                name,
                location
            )
        )

        connection.commit()

        return {
            "message": "Warehouse created successfully",
            "warehouse_id": cursor.lastrowid
        }

    except Exception as error:

        connection.rollback()

        return {
            "error": str(error)
        }

    finally:

        connection.close()


def get_warehouses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM warehouses
        ORDER BY id DESC
        """
    )

    warehouses = cursor.fetchall()

    connection.close()

    return [
        dict(warehouse)
        for warehouse in warehouses
    ]


def get_warehouse(warehouse_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM warehouses
        WHERE id = ?
        """,
        (warehouse_id,)
    )

    warehouse = cursor.fetchone()

    connection.close()

    if warehouse is None:
        return None

    return dict(warehouse)