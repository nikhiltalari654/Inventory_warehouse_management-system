from app.database import get_connection


def create_product(
    name,
    sku,
    description,
    price,
    reorder_level
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (
                name,
                sku,
                description,
                price,
                reorder_level
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                sku,
                description,
                price,
                reorder_level
            )
        )

        connection.commit()

        return {
            "message": "Product created successfully",
            "product_id": cursor.lastrowid
        }

    except Exception as error:

        connection.rollback()

        return {
            "error": str(error)
        }

    finally:

        connection.close()


def get_products():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY id DESC
        """
    )

    products = cursor.fetchall()

    connection.close()

    return [
        dict(product)
        for product in products
    ]


def get_product(product_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if product is None:
        return None

    return dict(product)


def delete_product(product_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted