from app.database import get_connection


def initialize_stock(
    product_id,
    warehouse_id,
    quantity
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO warehouse_stock
            (
                product_id,
                warehouse_id,
                current_stock
            )
            VALUES (?, ?, ?)
            """,
            (
                product_id,
                warehouse_id,
                quantity
            )
        )

        connection.commit()

        return {
            "message": "Stock initialized successfully"
        }

    except Exception as error:

        connection.rollback()

        return {
            "error": str(error)
        }

    finally:

        connection.close()


def get_all_stock():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            ws.id,
            p.name AS product_name,
            p.sku,
            w.name AS warehouse_name,
            w.location,
            ws.current_stock,
            p.reorder_level

        FROM warehouse_stock ws

        JOIN products p
            ON ws.product_id = p.id

        JOIN warehouses w
            ON ws.warehouse_id = w.id

        ORDER BY ws.id DESC
        """
    )

    stock = cursor.fetchall()

    connection.close()

    return [
        dict(item)
        for item in stock
    ]


def get_stock(
    warehouse_id,
    product_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            ws.current_stock,
            p.name AS product_name,
            p.reorder_level,
            w.name AS warehouse_name

        FROM warehouse_stock ws

        JOIN products p
            ON ws.product_id = p.id

        JOIN warehouses w
            ON ws.warehouse_id = w.id

        WHERE ws.warehouse_id = ?
        AND ws.product_id = ?
        """,
        (
            warehouse_id,
            product_id
        )
    )

    stock = cursor.fetchone()

    connection.close()

    if stock is None:
        return None

    return dict(stock)

def update_stock(
    connection,
    product_id,
    warehouse_id,
    quantity,
    movement_type,
    reference_type=None,
    reference_id=None
):

    cursor = connection.cursor()

    # Get current stock
    cursor.execute(
        """
        SELECT current_stock
        FROM warehouse_stock

        WHERE product_id = ?
        AND warehouse_id = ?
        """,
        (
            product_id,
            warehouse_id
        )
    )

    stock = cursor.fetchone()

    if stock is None:

        raise Exception(
            "Stock record not found"
        )

    current_stock = stock["current_stock"]

    # IN
    if movement_type == "IN":

        new_stock = (
            current_stock + quantity
        )

    # OUT
    elif movement_type == "OUT":

        if current_stock < quantity:

            raise Exception(
                "Insufficient stock"
            )

        new_stock = (
            current_stock - quantity
        )

    else:

        raise Exception(
            "Invalid movement type"
        )

    # Update stock
    cursor.execute(
        """
        UPDATE warehouse_stock

        SET current_stock = ?

        WHERE product_id = ?
        AND warehouse_id = ?
        """,
        (
            new_stock,
            product_id,
            warehouse_id
        )
    )

    # Record movement
    cursor.execute(
        """
        INSERT INTO stock_movements
        (
            product_id,
            warehouse_id,
            movement_type,
            quantity,
            reference_type,
            reference_id
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            product_id,
            warehouse_id,
            movement_type,
            quantity,
            reference_type,
            reference_id
        )
    )

    # Check reorder level
    cursor.execute(
        """
        SELECT
            name,
            reorder_level

        FROM products

        WHERE id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:

        raise Exception(
            "Product not found"
        )

    # Low stock
    if new_stock <= product["reorder_level"]:

        message = (
            f"Low stock alert: "
            f"{product['name']} "
            f"has only {new_stock} units."
        )

        cursor.execute(
            """
            INSERT INTO notifications
            (
                product_id,
                warehouse_id,
                notification_type,
                message
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                product_id,
                warehouse_id,
                "LOW_STOCK",
                message
            )
        )

    return new_stock