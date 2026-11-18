from app.database import get_connection
from app.stock import update_stock


def create_sales_order(
    customer_name,
    warehouse_id,
    product_id,
    quantity,
    unit_price
):

    connection = get_connection()

    try:

        connection.execute("BEGIN")

        cursor = connection.cursor()

        # Create sales order
        cursor.execute(
            """
            INSERT INTO sales_orders
            (
                customer_name,
                warehouse_id,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                customer_name,
                warehouse_id,
                "COMPLETED"
            )
        )

        sales_order_id = cursor.lastrowid

        # Create sales item
        cursor.execute(
            """
            INSERT INTO sales_order_items
            (
                sales_order_id,
                product_id,
                quantity,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                sales_order_id,
                product_id,
                quantity,
                unit_price
            )
        )

        # Reduce stock
        new_stock = update_stock(
            connection,
            product_id,
            warehouse_id,
            quantity,
            "OUT",
            "SALES_ORDER",
            sales_order_id
        )

        connection.commit()

        return {
            "message": "Sales order completed",
            "sales_order_id": sales_order_id,
            "new_stock": new_stock
        }

    except Exception as error:

        connection.rollback()

        return {
            "error": str(error)
        }

    finally:

        connection.close()


def get_sales_orders():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            so.id,
            so.customer_name,
            so.status,
            so.order_date,
            w.name AS warehouse_name

        FROM sales_orders so

        JOIN warehouses w
            ON so.warehouse_id = w.id

        ORDER BY so.id DESC
        """
    )

    orders = cursor.fetchall()

    connection.close()

    return [
        dict(order)
        for order in orders
    ]