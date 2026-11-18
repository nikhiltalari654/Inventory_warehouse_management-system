from app.database import get_connection


def get_notifications():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            n.id,
            n.notification_type,
            n.message,
            n.is_read,
            n.created_at,

            p.name AS product_name,

            w.name AS warehouse_name

        FROM notifications n

        JOIN products p
            ON n.product_id = p.id

        JOIN warehouses w
            ON n.warehouse_id = w.id

        ORDER BY n.id DESC
        """
    )

    notifications = cursor.fetchall()

    connection.close()

    return [
        dict(notification)
        for notification in notifications
    ]


def get_unread_notifications():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            n.id,
            n.notification_type,
            n.message,
            n.created_at,

            p.name AS product_name,

            w.name AS warehouse_name

        FROM notifications n

        JOIN products p
            ON n.product_id = p.id

        JOIN warehouses w
            ON n.warehouse_id = w.id

        WHERE n.is_read = 0

        ORDER BY n.id DESC
        """
    )

    notifications = cursor.fetchall()

    connection.close()

    return [
        dict(notification)
        for notification in notifications
    ]


def mark_as_read(notification_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE notifications

        SET is_read = 1

        WHERE id = ?
        """,
        (notification_id,)
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated