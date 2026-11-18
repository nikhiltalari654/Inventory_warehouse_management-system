from app.database import get_connection
from app.stock import update_stock


def create_purchase_order(
    supplier_name,
    warehouse_id,
    product_id,
    quantity,
    unit_price
):

    connection = get_connection()

    try:

        # Start transaction
        connection.execute("BEGIN")

        cursor = connection.cursor()

        # Create purchase order
        cursor.execute(
            """
            INSERT INTO purchase_orders
            (
                supplier_name,
                warehouse_id,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                supplier_name,
                warehouse_id,
                "COMPLETED"
            )
        )

        purchase_order_id = cursor.lastrowid

        # Create purchase item
        cursor.execute(
            """
            INSERT INTO purchase_order_items
            (
                purchase_order_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                purchase_order_id,
                product_id,
                quantity,
                unit_price
            )
        )

        # Add stock
        new_stock = update_stock(
            connection,
            product_id,
            warehouse_id,
            quantity,
            "IN",
            "PURCHASE_ORDER",
            purchase_order_id
        )

        connection.commit()

        return {
            "message": "Purchase order completed",
            "purchase_order_id": purchase_order_id,
            "new_stock": new_stock
        }

    except Exception as error:

        connection.rollback()

        return {
            "error": str(error)
        }

    finally:

        connection.close()


def get_purchase_orders():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            po.id,
            po.supplier_name,
            po.status,
            po.order_date,
            w.name AS warehouse_name

        FROM purchase_orders po

        JOIN warehouses w
            ON po.warehouse_id = w.id

        ORDER BY po.id DESC
        """
    )

    orders = cursor.fetchall()

    connection.close()

    return [
        dict(order)
        for order in orders
    ]