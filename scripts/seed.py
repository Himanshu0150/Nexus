import sys
import os
import random

# Add parent directory to path to import db queries
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.postgres_queries import (
    init_schema, delete_all_order_items, delete_all_orders, delete_all_addresses,
    delete_all_inventory, delete_all_users, insert_demo_user, add_user_address,
    insert_inventory_batch
)
from db.mongo_queries import delete_all_products, insert_many_products

# Use fixed random seed for reproducible data
random.seed(42)

# --- Real product names per category ---
PRODUCT_NAMES = {
    'laptops': [
        'MacBook Air M3', 'MacBook Pro 14"', 'Dell XPS 15', 'Dell XPS 13',
        'ThinkPad X1 Carbon', 'ThinkPad T14s', 'HP Spectre x360', 'HP Envy 16',
        'ASUS ZenBook Pro 14', 'ASUS ROG Zephyrus G14', 'Razer Blade 15',
        'Razer Book 13', 'Surface Laptop 5', 'Surface Pro 9', 'Acer Swift 5',
        'Acer Predator Helios 18', 'LG Gram 16', 'Samsung Galaxy Book4 Pro',
        'Lenovo IdeaPad Slim 5', 'Lenovo Legion 5i Pro', 'MSI Stealth 16 Studio',
        'HP EliteBook 840 G10', 'ASUS VivoBook 15', 'Huawei MateBook X Pro',
        'Framework Laptop 13',
    ],
    'shoes': [
        'Nike Air Max 270', 'Nike React Infinity Run', 'Adidas Ultraboost 23',
        'Adidas Stan Smith', 'New Balance 990v6', 'Converse Chuck Taylor',
        'Vans Old Skool', 'Puma RS-X', 'Reebok Classic Leather',
        'Air Jordan 1 Retro High', 'Brooks Ghost 15', 'ASICS Gel-Nimbus 25',
        'Saucony Ride 16', 'On Cloudmonster', 'Hoka Clifton 9',
        'Salomon Speedcross 6', 'Merrell Moab 3 GTX', 'Timberland 6-Inch Boot',
        'Dr. Martens 1460', 'Birkenstock Arizona', 'Allbirds Tree Runner',
        'Veja V-10 Leather', 'New Balance 574', 'Nike Pegasus 40',
        'Adidas Campus 00s',
    ],
    'books': [
        'The Pragmatic Programmer', 'Clean Code', 'Designing Data-Intensive Apps',
        'The Psychology of Money', 'Atomic Habits', 'Sapiens', 'Dune', '1984',
        'The Alchemist', 'Thinking, Fast and Slow', 'Zero to One',
        'Rich Dad Poor Dad', 'The Lean Startup', 'Deep Work',
        'A Brief History of Time', 'The Art of War', "Ender's Game",
        'Neuromancer', "The Hitchhiker's Guide to the Galaxy",
        'The Lord of the Rings', "Harry Potter: Sorcerer's Stone",
        'The Great Gatsby', 'To Kill a Mockingbird', 'Cosmos',
        "Man's Search for Meaning",
    ],
    'phones': [
        'iPhone 15 Pro Max', 'iPhone 15 Pro', 'Samsung Galaxy S24 Ultra',
        'Samsung Galaxy S24+', 'Google Pixel 8 Pro', 'Google Pixel 8a',
        'OnePlus 12', 'Xiaomi 14 Ultra', 'Sony Xperia 1 VI',
        'Motorola Edge 50 Pro', 'Nothing Phone 2a', 'Samsung Galaxy Z Fold 6',
        'Samsung Galaxy Z Flip 6', 'ASUS ROG Phone 8 Pro', 'Vivo X100 Pro',
        'Oppo Find X7 Ultra', 'Realme GT 6', 'Honor Magic 6 Pro',
        'iPhone 15', 'iPhone SE 3rd Gen', 'Samsung Galaxy A55',
        'Google Pixel 8', 'Motorola G Power 2024', 'Xiaomi Redmi Note 13 Pro',
        'OnePlus Nord 4',
    ],
}

# --- Attribute configs per category ---
LAPTOP_ATTRS  = [('8GB','i5'), ('8GB','i7'), ('16GB','i5'), ('16GB','i7'),
                 ('16GB','M1'), ('16GB','M2'), ('32GB','i7'), ('32GB','M2')]
SHOE_SIZES    = range(6, 13)
SHOE_COLORS   = ['Black', 'White', 'Navy', 'Red', 'Grey', 'Olive', 'Brown', 'Blue']
PHONE_CONFIGS = [('128GB','12MP'), ('128GB','48MP'), ('256GB','48MP'),
                 ('256GB','108MP'), ('512GB','48MP'), ('512GB','108MP')]

def make_description(category, attributes):
    if category == 'laptops':
        return f"Powered by {attributes['cpu']} with {attributes['ram']} RAM — built for speed and reliability."
    if category == 'shoes':
        return f"Crafted in sleek {attributes['color']}, size {attributes['size']} — comfort meets style."
    if category == 'books':
        return f"A {attributes['pages']}-page journey by {attributes['author']}. A must-read."
    if category == 'phones':
        return f"{attributes['storage']} of storage and a {attributes['camera']} camera — capture every moment."
    return "A premium product."

def make_image_url(product_id_num, category):
    keyword = {'laptops': 'laptop', 'shoes': 'shoes', 'books': 'book', 'phones': 'smartphone'}[category]
    return f"https://loremflickr.com/400/300/{keyword}?lock={product_id_num}"

def generate_product(product_id_num, category, name_index):
    product_id = f"P{product_id_num:04d}"
    name       = PRODUCT_NAMES[category][name_index]
    price      = round(random.uniform(10.0, 2000.0), 2)

    if category == 'laptops':
        ram, cpu = random.choice(LAPTOP_ATTRS)
        attributes = {'ram': ram, 'cpu': cpu}
    elif category == 'shoes':
        attributes = {'size': random.choice(list(SHOE_SIZES)),
                      'color': random.choice(SHOE_COLORS)}
    elif category == 'books':
        attributes = {'author': f"Author {random.randint(1, 100)}",
                      'pages': random.randint(100, 1000)}
    elif category == 'phones':
        storage, camera = random.choice(PHONE_CONFIGS)
        attributes = {'storage': storage, 'camera': camera}
    else:
        attributes = {}

    reviews = []
    for _ in range(random.randint(0, 3)):
        reviews.append({
            'user':   f"User{random.randint(1, 20)}",
            'rating': random.randint(1, 5),
            'text':   random.choice([
                "Great product!", "Not bad.", "Highly recommend!",
                "Good value for money.", "Exceeded my expectations.",
                "Would buy again.", "Decent quality.",
            ])
        })

    return {
        'product_id':  product_id,
        'name':        name,
        'category':    category,
        'price':       price,
        'description': make_description(category, attributes),
        'attributes':  attributes,
        'reviews':     reviews,
        'image_url':   make_image_url(product_id_num, category),
    }

def main():
    print("Initializing / migrating database schema...")
    init_schema()

    print("Clearing existing data...")
    delete_all_order_items()
    delete_all_orders()
    delete_all_addresses()
    delete_all_inventory()
    delete_all_users()
    delete_all_products()

    print("Seeding exactly 1 Demo User (demo@nexus.com / demo123)...")
    demo_user_id = insert_demo_user("Demo User", "demo@nexus.com", "demo123")
    
    print("Seeding default address for Demo User...")
    add_user_address(
        user_id=demo_user_id,
        label="Home (Primary)",
        recipient_name="Demo User",
        street="742 Evergreen Terrace",
        city="Springfield",
        state="OR",
        postal_code="97477",
        is_default=True
    )
    add_user_address(
        user_id=demo_user_id,
        label="Work / Office",
        recipient_name="Demo User",
        street="100 Silicon Parkway, Suite 400",
        city="San Jose",
        state="CA",
        postal_code="95134",
        is_default=False
    )

    print("Generating 100 products (25 per category) and inventory...")
    products_to_insert = []
    inventory_data = []

    categories = ['laptops', 'shoes', 'books', 'phones']
    product_id_num = 1
    for category in categories:
        for name_index in range(25):
            prod = generate_product(product_id_num, category, name_index)
            products_to_insert.append(prod)
            inventory_data.append((prod['product_id'], random.randint(5, 50)))
            product_id_num += 1

    insert_inventory_batch(inventory_data)
    insert_many_products(products_to_insert)

    print("Generating product SVG images in MongoDB...")
    from scripts.fetch_images import main as seed_images
    seed_images()

    print(f"Seeded 1 Demo User (ID: {demo_user_id}) and 2 sample addresses in PostgreSQL.")
    print(f"Seeded {len(inventory_data)} inventory records in PostgreSQL.")
    print(f"Seeded {len(products_to_insert)} products in MongoDB.")

if __name__ == "__main__":
    main()
