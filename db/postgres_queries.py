import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_pg_connection():
    uri = os.environ.get("POSTGRES_URI") or "postgresql://postgres:postgres@localhost:5432/postgres"
    return psycopg2.connect(uri)

# Check postgres connection
def check_connection():
    with get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            return cur.fetchone()

# Initialize or migrate database schema
def init_schema():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT DEFAULT 'demo123',
                created_at TIMESTAMP DEFAULT now()
            );
            ALTER TABLE users ADD COLUMN IF NOT EXISTS password TEXT DEFAULT 'demo123';
            ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT now();
            CREATE TABLE IF NOT EXISTS addresses (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                label TEXT,
                recipient_name TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                postal_code TEXT,
                country TEXT DEFAULT 'United States',
                is_default BOOLEAN DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS inventory (
                product_id TEXT PRIMARY KEY,
                stock INT CHECK (stock >= 0)
            );
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                total NUMERIC,
                status TEXT,
                shipping_address TEXT,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT now()
            );
            ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_address TEXT;
            ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method TEXT;
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INT REFERENCES orders(id),
                product_id TEXT,
                product_name TEXT,
                price NUMERIC,
                qty INT
            );
        """)
        conn.commit()

# Delete all order items
def delete_all_order_items():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE order_items RESTART IDENTITY CASCADE;")
        conn.commit()

# Delete all orders
def delete_all_orders():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE orders RESTART IDENTITY CASCADE;")
        conn.commit()

# Delete all addresses
def delete_all_addresses():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE addresses RESTART IDENTITY CASCADE;")
        conn.commit()

# Delete all inventory
def delete_all_inventory():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE inventory CASCADE;")
        conn.commit()

# Delete all users
def delete_all_users():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
        conn.commit()

# Get all users
def get_users():
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, email FROM users ORDER BY id ASC;")
        return cur.fetchall()

# Find user by email
def get_user_by_email(email):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, email, password FROM users WHERE LOWER(email) = LOWER(%s);", (email.strip(),))
        return cur.fetchone()

# Find user by ID
def get_user_by_id(user_id):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, email, created_at FROM users WHERE id = %s;", (user_id,))
        return cur.fetchone()

# Register new user
def create_user(name, email, password):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id, name, email;", (name.strip(), email.strip().lower(), password))
        conn.commit()
        return cur.fetchone()

# Update user profile
def update_user_profile(user_id, name, email):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id, name, email;", (name, email, user_id))
        conn.commit()
        return cur.fetchone()

# Insert single demo user
def insert_demo_user(name, email, password):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;", (name, email, password))
        conn.commit()
        return cur.fetchone()['id']

# Get addresses for a user
def get_user_addresses(user_id):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM addresses WHERE user_id = %s ORDER BY is_default DESC, id DESC;", (user_id,))
        return cur.fetchall()

# Add an address for a user
def add_user_address(user_id, label, recipient_name, street, city, state, postal_code, is_default=False):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        if is_default:
            cur.execute("UPDATE addresses SET is_default = FALSE WHERE user_id = %s;", (user_id,))
        cur.execute("""
            INSERT INTO addresses (user_id, label, recipient_name, street, city, state, postal_code, is_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (user_id, label, recipient_name, street, city, state, postal_code, is_default))
        conn.commit()
        return cur.fetchone()['id']

# Delete address by ID
def delete_user_address(address_id, user_id):
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM addresses WHERE id = %s AND user_id = %s;", (address_id, user_id))
        conn.commit()

# Set an address as default
def set_default_address(address_id, user_id):
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("UPDATE addresses SET is_default = FALSE WHERE user_id = %s;", (user_id,))
        cur.execute("UPDATE addresses SET is_default = TRUE WHERE id = %s AND user_id = %s;", (address_id, user_id))
        conn.commit()

# Insert multiple inventory records
def insert_inventory_batch(inventory_data):
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.executemany("INSERT INTO inventory (product_id, stock) VALUES (%s, %s);", inventory_data)
        conn.commit()

# Get product stock
def get_inventory_stock(product_id):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT stock FROM inventory WHERE product_id = %s;", (product_id,))
        return cur.fetchone()

# Get orders by user ID
def get_orders_by_user(user_id):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, user_id, total, status, shipping_address, payment_method, created_at FROM orders WHERE user_id = %s ORDER BY id DESC;", (user_id,))
        return cur.fetchall()

# Get order items by order ID
def get_order_items(order_id):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM order_items WHERE order_id = %s;", (order_id,))
        return cur.fetchall()

# Update stock directly with cursor
def _update_stock(cur, item):
    cur.execute("UPDATE inventory SET stock = stock - %s WHERE product_id = %s AND stock >= %s;", (item['qty'], item['product_id'], item['qty']))
    return cur.rowcount

# Insert order directly with cursor
def _insert_order(cur, user_id, total, shipping_address, payment_method):
    cur.execute("""
        INSERT INTO orders (user_id, total, status, shipping_address, payment_method)
        VALUES (%s, %s, 'completed', %s, %s) RETURNING id;
    """, (user_id, total, shipping_address, payment_method))
    row = cur.fetchone()
    return row['id'] if isinstance(row, dict) else row[0]

# Insert order item directly with cursor
def _insert_order_item(cur, order_id, item):
    cur.execute("INSERT INTO order_items (order_id, product_id, product_name, price, qty) VALUES (%s, %s, %s, %s, %s);", (order_id, item['product_id'], item['name'], item['price'], item['qty']))

# Process full order transaction
def place_order_transaction(user_id, total, items, shipping_address="Standard Address", payment_method="Credit Card"):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        for item in items:
            if _update_stock(cur, item) == 0:
                conn.rollback()
                raise Exception(f"Insufficient stock for {item['product_id']}")
        order_id = _insert_order(cur, user_id, total, shipping_address, payment_method)
        for item in items:
            _insert_order_item(cur, order_id, item)
        conn.commit()
        return order_id

# Force stock to a specific value for testing
def force_stock(product_id, stock):
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("UPDATE inventory SET stock = %s WHERE product_id = %s;", (stock, product_id))
        conn.commit()

# Get a single random product ID
def get_random_product_id():
    with get_pg_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT product_id FROM inventory LIMIT 1;")
        row = cur.fetchone()
        return row['product_id'] if isinstance(row, dict) else row[0]
