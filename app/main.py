from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import create_tables

import app.auth as auth
import app.products as products
import app.warehouses as warehouses
import app.stock as stock
import app.purchase_orders as purchase_orders
import app.sales_orders as sales_orders
import app.notifications as notifications


app = FastAPI(
    title="Inventory & Warehouse Management System",
    version="1.0.0"
)


# =========================================
# CREATE TABLES
# =========================================

create_tables()


# =========================================
# REGISTER REQUEST
# =========================================

class RegisterRequest(BaseModel):

    username: str
    password: str


# =========================================
# LOGIN REQUEST
# =========================================

class LoginRequest(BaseModel):

    username: str
    password: str


# =========================================
# PRODUCT REQUEST
# =========================================

class ProductRequest(BaseModel):

    name: str
    sku: str
    description: str | None = None
    price: float
    reorder_level: int = 10


# =========================================
# WAREHOUSE REQUEST
# =========================================

class WarehouseRequest(BaseModel):

    name: str
    location: str


# =========================================
# STOCK REQUEST
# =========================================

class StockRequest(BaseModel):

    product_id: int
    warehouse_id: int
    quantity: int


# =========================================
# PURCHASE REQUEST
# =========================================

class PurchaseRequest(BaseModel):

    supplier_name: str
    warehouse_id: int
    product_id: int
    quantity: int
    unit_price: float


# =========================================
# SALES REQUEST
# =========================================

class SalesRequest(BaseModel):

    customer_name: str
    warehouse_id: int
    product_id: int
    quantity: int
    unit_price: float


# =========================================
# REGISTER
# =========================================

@app.post("/register")
def register(data: RegisterRequest):

    result = auth.register(
        data.username,
        data.password
    )

    if "error" in result:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


# =========================================
# LOGIN
# =========================================

@app.post("/login")
def login(data: LoginRequest):

    result = auth.login(
        data.username,
        data.password
    )

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "username": result["username"]
    }


# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "Inventory Management API is running"
    }


# =========================================
# PRODUCTS
# =========================================

@app.post("/products")
def create_product(data: ProductRequest):

    result = products.create_product(
        data.name,
        data.sku,
        data.description,
        data.price,
        data.reorder_level
    )

    if "error" in result:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.get("/products")
def get_products():

    return products.get_products()


@app.get("/products/{product_id}")
def get_product(product_id: int):

    result = products.get_product(product_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return result


@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    result = products.delete_product(product_id)

    if result == 0:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }


# =========================================
# WAREHOUSES
# =========================================

@app.post("/warehouses")
def create_warehouse(data: WarehouseRequest):

    result = warehouses.create_warehouse(
        data.name,
        data.location
    )

    if "error" in result:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.get("/warehouses")
def get_warehouses():

    return warehouses.get_warehouses()


@app.get("/warehouses/{warehouse_id}")
def get_warehouse(warehouse_id: int):

    result = warehouses.get_warehouse(
        warehouse_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    return result


# =========================================
# STOCK
# =========================================

@app.post("/stock")
def add_stock(data: StockRequest):

    result = stock.initialize_stock(
        data.product_id,
        data.warehouse_id,
        data.quantity
    )

    if "error" in result:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.get("/stock")
def get_all_stock():

    return stock.get_all_stock()


@app.get("/stock/{warehouse_id}/{product_id}")
def get_stock(
    warehouse_id: int,
    product_id: int
):

    result = stock.get_stock(
        warehouse_id,
        product_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )

    return result


# =========================================
# PURCHASE ORDERS
# =========================================

@app.post("/purchase-orders")
def create_purchase_order(
    data: PurchaseRequest
):

    result = purchase_orders.create_purchase_order(
        data.supplier_name,
        data.warehouse_id,
        data.product_id,
        data.quantity,
        data.unit_price
    )

    if "error" in result:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.get("/purchase-orders")
def get_purchase_orders():

    return purchase_orders.get_purchase_orders()


# =========================================
# SALES ORDERS
# =========================================

@app.post("/sales-orders")
def create_sales_order(
    data: SalesRequest
):

    result = sales_orders.create_sales_order(
        data.customer_name,
        data.warehouse_id,
        data.product_id,
        data.quantity,
        data.unit_price
    )

    if "error" in result:

        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    return result


@app.get("/sales-orders")
def get_sales_orders():

    return sales_orders.get_sales_orders()


# =========================================
# NOTIFICATIONS
# =========================================

@app.get("/notifications")
def get_notifications():

    return notifications.get_notifications()


@app.get("/notifications/unread")
def get_unread_notifications():

    return notifications.get_unread_notifications()


@app.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int
):

    result = notifications.mark_as_read(
        notification_id
    )
    if result == 0:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification marked as read"
    }