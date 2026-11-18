import streamlit as st
import requests


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------


API_URL = "https://inventory-warehouse-management-system-jos6.onrender.com"


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)


# --------------------------------------------------
# REGISTER PAGE
# --------------------------------------------------

def register_page():

    st.title("📦 Inventory Management System")
    st.subheader("Create Account")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if username == "" or password == "":
            st.error("Please enter username and password")

        elif password != confirm_password:
            st.error("Passwords do not match")

        else:

            response = requests.post(
                f"{API_URL}/register",
                json={
                    "username": username,
                    "password": password
                }
            )

            if response.status_code == 200:

                st.success(
                    "Registration successful. Please login."
                )

                st.session_state.show_login = True

            else:

                st.error(
                    response.json().get(
                        "detail",
                        "Registration failed"
                    )
                )


# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

def login_page():

    st.title("📦 Inventory Management System")
    st.subheader("Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "" or password == "":
            st.error("Please enter username and password")
            return

        response = requests.post(
            f"{API_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.session_state.logged_in = True
            st.session_state.username = result["username"]

            st.success("Login successful")

            st.rerun()

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Invalid username or password"
                )
            )


# --------------------------------------------------
# PRODUCT PAGE
# --------------------------------------------------

def product_page():

    st.header("📦 Products")

    st.subheader("Add Product")

    name = st.text_input("Product Name")
    sku = st.text_input("SKU")
    description = st.text_area("Description")
    price = st.number_input(
        "Price",
        min_value=0.0,
        step=1.0
    )
    reorder_level = st.number_input(
        "Reorder Level",
        min_value=0,
        value=10,
        step=1
    )

    if st.button("Add Product"):

        response = requests.post(
            f"{API_URL}/products",
            json={
                "name": name,
                "sku": sku,
                "description": description,
                "price": price,
                "reorder_level": reorder_level
            }
        )

        if response.status_code == 200:

            st.success("Product added successfully")

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Failed to add product"
                )
            )

    st.subheader("Product List")

    response = requests.get(
        f"{API_URL}/products"
    )

    if response.status_code == 200:

        products = response.json()

        if products:
            st.dataframe(
                products,
                use_container_width=True
            )
        else:
            st.info("No products found")


# --------------------------------------------------
# WAREHOUSE PAGE
# --------------------------------------------------

def warehouse_page():

    st.header("🏭 Warehouses")

    st.subheader("Add Warehouse")

    name = st.text_input(
        "Warehouse Name"
    )

    location = st.text_input(
        "Location"
    )

    if st.button("Add Warehouse"):

        response = requests.post(
            f"{API_URL}/warehouses",
            json={
                "name": name,
                "location": location
            }
        )

        if response.status_code == 200:

            st.success(
                "Warehouse added successfully"
            )

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Failed to add warehouse"
                )
            )

    st.subheader("Warehouse List")

    response = requests.get(
        f"{API_URL}/warehouses"
    )

    if response.status_code == 200:

        warehouses = response.json()

        if warehouses:
            st.dataframe(
                warehouses,
                use_container_width=True
            )
        else:
            st.info("No warehouses found")


# --------------------------------------------------
# STOCK PAGE
# --------------------------------------------------

def stock_page():

    st.header("📊 Stock Management")

    st.subheader("Initialize Stock")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1
    )

    warehouse_id = st.number_input(
        "Warehouse ID",
        min_value=1,
        step=1
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0,
        step=1
    )

    if st.button("Add Stock"):

        response = requests.post(
            f"{API_URL}/stock",
            json={
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "quantity": quantity
            }
        )

        if response.status_code == 200:

            st.success(
                "Stock initialized successfully"
            )

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Failed to add stock"
                )
            )

    st.subheader("Current Stock")

    response = requests.get(
        f"{API_URL}/stock"
    )

    if response.status_code == 200:

        stock = response.json()

        if stock:
            st.dataframe(
                stock,
                use_container_width=True
            )
        else:
            st.info("No stock records found")


# --------------------------------------------------
# PURCHASE ORDER PAGE
# --------------------------------------------------

def purchase_order_page():

    st.header("🛒 Purchase Orders")

    supplier_name = st.text_input(
        "Supplier Name"
    )

    warehouse_id = st.number_input(
        "Warehouse ID",
        min_value=1,
        step=1,
        key="purchase_warehouse"
    )

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1,
        key="purchase_product"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1,
        key="purchase_quantity"
    )

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        step=1.0,
        key="purchase_price"
    )

    if st.button("Create Purchase Order"):

        response = requests.post(
            f"{API_URL}/purchase-orders",
            json={
                "supplier_name": supplier_name,
                "warehouse_id": warehouse_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.success(
                result["message"]
            )

            st.write(
                "New Stock:",
                result["new_stock"]
            )

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Purchase order failed"
                )
            )

    st.subheader("Purchase Orders")

    response = requests.get(
        f"{API_URL}/purchase-orders"
    )

    if response.status_code == 200:

        orders = response.json()

        if orders:
            st.dataframe(
                orders,
                use_container_width=True
            )
        else:
            st.info("No purchase orders found")


# --------------------------------------------------
# SALES ORDER PAGE
# --------------------------------------------------

def sales_order_page():

    st.header("💰 Sales Orders")

    customer_name = st.text_input(
        "Customer Name"
    )

    warehouse_id = st.number_input(
        "Warehouse ID",
        min_value=1,
        step=1,
        key="sales_warehouse"
    )

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1,
        key="sales_product"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1,
        key="sales_quantity"
    )

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        step=1.0,
        key="sales_price"
    )

    if st.button("Create Sales Order"):

        response = requests.post(
            f"{API_URL}/sales-orders",
            json={
                "customer_name": customer_name,
                "warehouse_id": warehouse_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price
            }
        )

        if response.status_code == 200:

            result = response.json()

            st.success(
                result["message"]
            )

            st.write(
                "Remaining Stock:",
                result["new_stock"]
            )

        else:

            st.error(
                response.json().get(
                    "detail",
                    "Sales order failed"
                )
            )

    st.subheader("Sales Orders")

    response = requests.get(
        f"{API_URL}/sales-orders"
    )

    if response.status_code == 200:

        orders = response.json()

        if orders:
            st.dataframe(
                orders,
                use_container_width=True
            )
        else:
            st.info("No sales orders found")


# --------------------------------------------------
# NOTIFICATION PAGE
# --------------------------------------------------

def notification_page():

    st.header("🔔 Notifications")

    response = requests.get(
        f"{API_URL}/notifications"
    )

    if response.status_code == 200:

        notifications = response.json()

        if notifications:

            for notification in notifications:

                if notification["is_read"] == 0:

                    st.warning(
                        notification["message"]
                    )

                    if st.button(
                        "Mark as Read",
                        key=f"read_{notification['id']}"
                    ):

                        requests.put(
                            f"{API_URL}/notifications/"
                            f"{notification['id']}/read"
                        )

                        st.rerun()

                else:

                    st.info(
                        notification["message"]
                    )

        else:

            st.success(
                "No notifications"
            )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

def dashboard():

    st.sidebar.title("📦 Inventory System")

    st.sidebar.write(
        f"Welcome, **{st.session_state.username}**"
    )

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Products",
            "Warehouses",
            "Stock",
            "Purchase Orders",
            "Sales Orders",
            "Notifications"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = None

        st.rerun()

    if page == "Dashboard":

        st.title("📦 Inventory Dashboard")

        st.success(
            f"Welcome {st.session_state.username}!"
        )

        st.write(
            "Use the sidebar to manage your inventory."
        )

        col1, col2, col3 = st.columns(3)

        response = requests.get(
            f"{API_URL}/products"
        )

        if response.status_code == 200:

            products = response.json()

            col1.metric(
                "Products",
                len(products)
            )

        response = requests.get(
            f"{API_URL}/warehouses"
        )

        if response.status_code == 200:

            warehouses = response.json()

            col2.metric(
                "Warehouses",
                len(warehouses)
            )

        response = requests.get(
            f"{API_URL}/notifications/unread"
        )

        if response.status_code == 200:

            notifications = response.json()

            col3.metric(
                "Unread Alerts",
                len(notifications)
            )

    elif page == "Products":
        product_page()

    elif page == "Warehouses":
        warehouse_page()

    elif page == "Stock":
        stock_page()

    elif page == "Purchase Orders":
        purchase_order_page()

    elif page == "Sales Orders":
        sales_order_page()

    elif page == "Notifications":
        notification_page()


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if "show_login" not in st.session_state:
    st.session_state.show_login = True


if not st.session_state.logged_in:

    option = st.radio(
        "Choose an option",
        [
            "Login",
            "Register"
        ],
        horizontal=True
    )

    if option == "Login":
        login_page()

    else:
        register_page()

else:

    dashboard()
