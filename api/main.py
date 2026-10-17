from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import datetime

from db.mongo_queries import search_products, get_product_by_id, get_products_by_ids, get_product_image_data
from db.postgres_queries import (
    get_inventory_stock, place_order_transaction, get_orders_by_user,
    get_order_items, get_users, get_user_by_email, get_user_by_id,
    create_user, update_user_profile, get_user_addresses,
    add_user_address, delete_user_address, set_default_address
)
from db.chroma_queries import get_similar_product_ids, query_by_text

app = FastAPI()

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/health")
def get_health():
    return {"status": "ok", "service": "Nexus Electronics API"}

@app.get("/store")
def get_storefront():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Storefront not found")


# Store last 20 requests
request_log = []

def log_request(endpoint: str, store: str, query_text: str):
    request_log.append({
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "endpoint": endpoint, 
        "store": store, 
        "query_text": query_text
    })
    if len(request_log) > 20:
        request_log.pop(0)

# --- Pydantic Request Models ---
class RegisterInput(BaseModel):
    name: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

class UserProfileUpdateInput(BaseModel):
    name: str
    email: str

class AddressInput(BaseModel):
    label: str
    recipient_name: str
    street: str
    city: str
    state: str
    postal_code: str
    is_default: bool = False

class OrderItemInput(BaseModel):
    product_id: str
    qty: int

class OrderInput(BaseModel):
    user_id: int
    items: List[OrderItemInput]
    shipping_address: Optional[str] = "Standard Address"
    payment_method: Optional[str] = "Credit Card (Nexus Pay)"


# --- Basic & Auth Endpoints ---
@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/auth/register")
def register_user(payload: RegisterInput):
    clean_name = payload.name.strip()
    clean_email = payload.email.strip().lower()
    clean_pass = payload.password.strip()
    if not clean_name or not clean_email or not clean_pass:
        raise HTTPException(status_code=400, detail="Name, email, and password are required.")
    log_request("POST /auth/register", "Postgres", f"email={clean_email}")
    existing = get_user_by_email(clean_email)
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    user = create_user(clean_name, clean_email, clean_pass)
    return {"user": user, "message": "Account registered successfully."}

@app.post("/auth/login")
def login_user(payload: LoginInput):
    clean_email = payload.email.strip().lower()
    clean_pass = payload.password.strip()
    log_request("POST /auth/login", "Postgres", f"email={clean_email}")
    user = get_user_by_email(clean_email)
    if not user or user["password"] != clean_pass:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        },
        "message": "Login successful."
    }

@app.get("/users")
def get_users_endpoint():
    log_request("GET /users", "Postgres", "all")
    return get_users()

@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int):
    log_request(f"GET /users/{user_id}", "Postgres", f"id={user_id}")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, payload: UserProfileUpdateInput):
    log_request(f"PUT /users/{user_id}", "Postgres", f"name={payload.name}, email={payload.email}")
    updated = update_user_profile(user_id, payload.name, payload.email)
    return updated

# --- Address Management Endpoints ---
@app.get("/users/{user_id}/addresses")
def get_addresses_endpoint(user_id: int):
    log_request(f"GET /users/{user_id}/addresses", "Postgres", f"user_id={user_id}")
    return get_user_addresses(user_id)

@app.post("/users/{user_id}/addresses")
def add_address_endpoint(user_id: int, payload: AddressInput):
    log_request(f"POST /users/{user_id}/addresses", "Postgres", f"label={payload.label}")
    addr_id = add_user_address(
        user_id, payload.label, payload.recipient_name, payload.street,
        payload.city, payload.state, payload.postal_code, payload.is_default
    )
    return {"id": addr_id, "address_id": addr_id, "status": "created"}

@app.delete("/users/{user_id}/addresses/{address_id}")
def delete_address_endpoint(user_id: int, address_id: int):
    log_request(f"DELETE /users/{user_id}/addresses/{address_id}", "Postgres", f"addr={address_id}")
    delete_user_address(address_id, user_id)
    return {"status": "deleted"}

@app.put("/users/{user_id}/addresses/{address_id}/default")
def set_default_address_endpoint(user_id: int, address_id: int):
    log_request(f"PUT /users/{user_id}/addresses/{address_id}/default", "Postgres", f"addr={address_id}")
    set_default_address(address_id, user_id)
    return {"status": "default updated"}

# --- Products Endpoints ---
@app.get("/products")
def get_products(category: Optional[str] = None, q: Optional[str] = None, mode: Optional[str] = "keyword"):
    if q and mode == "vector":
        log_request("GET /products", "ChromaDB Vector", f"q={q}")
        pids = query_by_text(q, limit=25)
        if not pids:
            return []
        products = get_products_by_ids(pids)
        prod_map = {p["product_id"]: p for p in products}
        res = [prod_map[pid] for pid in pids if pid in prod_map]
        if category:
            res = [p for p in res if p.get("category") == category]
        return res
    
    log_request("GET /products", "Mongo", f"category={category}, q={q}")
    res = search_products(category, q, 100)
    # If standard keyword search on MongoDB returned 0 results but the user typed a query,
    # automatically perform vector semantic search as an intelligent fallback
    if not res and q:
        log_request("GET /products (fallback)", "ChromaDB Vector", f"q={q}")
        pids = query_by_text(q, limit=25)
        if pids:
            products = get_products_by_ids(pids)
            prod_map = {p["product_id"]: p for p in products}
            res = [prod_map[pid] for pid in pids if pid in prod_map]
            if category:
                res = [p for p in res if p.get("category") == category]
    return res

@app.get("/products/{product_id}")
def get_product(product_id: str):
    log_request(f"GET /products/{product_id}", "Mongo+Postgres", f"id={product_id}")
    prod = get_product_by_id(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    
    stock_record = get_inventory_stock(product_id)
    prod['stock'] = stock_record['stock'] if stock_record else 0
    return prod

@app.get("/products/{product_id}/image")
def get_product_image(product_id: str):
    doc = get_product_image_data(product_id)
    if not doc or not doc.get("image_data"):
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=bytes(doc["image_data"]), media_type=doc.get("image_mime", "image/jpeg"))

@app.get("/products/{product_id}/similar")
def get_similar(product_id: str):
    log_request(f"GET /products/{product_id}/similar", "vector", f"product_id={product_id}")
    similar_ids = get_similar_product_ids(product_id, 5)
    if not similar_ids:
        return []
    
    products = get_products_by_ids(similar_ids)
    prod_map = {p["product_id"]: p for p in products}
    return [prod_map[pid] for pid in similar_ids if pid in prod_map]

# --- Orders Endpoints ---
@app.post("/orders")
def create_order(order: OrderInput):
    log_request("POST /orders", "Mongo+Postgres", f"user={order.user_id}, items={len(order.items)}")
    
    enriched_items = []
    total = 0.0
    for item in order.items:
        prod = get_product_by_id(item.product_id)
        if not prod:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found")
        
        enriched_items.append({
            "product_id": item.product_id,
            "qty": item.qty,
            "name": prod["name"],
            "price": prod["price"]
        })
        total += float(prod["price"]) * item.qty
        
    try:
        order_id = place_order_transaction(
            user_id=order.user_id,
            total=total,
            items=enriched_items,
            shipping_address=order.shipping_address,
            payment_method=order.payment_method
        )
        return {"order_id": order_id, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders")
def get_orders(user_id: int):
    log_request("GET /orders", "Postgres", f"user_id={user_id}")
    return get_orders_by_user(user_id)

@app.get("/orders/{order_id}/items")
def get_order_items_endpoint(order_id: int):
    log_request(f"GET /orders/{order_id}/items", "Postgres", f"order_id={order_id}")
    return get_order_items(order_id)

@app.get("/debug/requests")
def get_debug_requests():
    return {"requests": request_log}
