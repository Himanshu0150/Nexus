import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    uri = os.environ.get("MONGO_URI") or "mongodb://localhost:27017/"
    return MongoClient(uri)

# Check mongo connection
def check_connection():
    client = get_mongo_client()
    return client.admin.command('ping')

# Delete all products
def delete_all_products():
    client = get_mongo_client()
    db = client["shop"]
    db.products.delete_many({})

# Insert multiple products
def insert_many_products(products):
    client = get_mongo_client()
    db = client["shop"]
    db.products.insert_many(products)

# Find products by category and text regex in name or description
def search_products(category=None, q=None, limit=20):
    client = get_mongo_client()
    db = client["shop"]
    filter_doc = {}
    if category: filter_doc['category'] = category
    if q: filter_doc['$or'] = [{'name': {'$regex': q, '$options': 'i'}}, {'description': {'$regex': q, '$options': 'i'}}]
    return list(db.products.find(filter_doc, {'_id': 0}).sort('price', 1).limit(limit))

# Find a single product by ID
def get_product_by_id(product_id):
    client = get_mongo_client()
    db = client["shop"]
    return db.products.find_one({'product_id': product_id}, {'_id': 0})

# Find multiple products by a list of IDs
def get_products_by_ids(product_ids):
    client = get_mongo_client()
    db = client["shop"]
    return list(db.products.find({'product_id': {'$in': product_ids}}, {'_id': 0}))

# Explain search query performance under the ESR rule
def explain_search_performance(category="laptops", sort_dir=1, min_price=None, max_price=None):
    client = get_mongo_client()
    db = client["shop"]
    query = {"category": category}
    if min_price is not None or max_price is not None:
        price_cond = {}
        if min_price is not None: price_cond["$gte"] = float(min_price)
        if max_price is not None: price_cond["$lte"] = float(max_price)
        query["price"] = price_cond
    return db.products.find(query).sort("price", sort_dir).explain()["executionStats"]

# Create an index for category and price
def create_category_price_index():
    client = get_mongo_client()
    db = client["shop"]
    db.products.create_index([("category", 1), ("price", 1)])

# Drop the category price index
def drop_category_price_index():
    client = get_mongo_client()
    db = client["shop"]
    try:
        db.products.drop_index("category_1_price_1")
    except Exception:
        pass

# Get a small sample of products
def get_sample_products(limit=5):
    client = get_mongo_client()
    db = client["shop"]
    return list(db.products.find({}, {"_id": 0}).limit(limit))

# Store raw image bytes for a product (as binary in the document)
def store_product_image(product_id, image_bytes, mime_type="image/jpeg"):
    client = get_mongo_client()
    db = client["shop"]
    db.products.update_one(
        {"product_id": product_id},
        {"$set": {"image_data": image_bytes, "image_mime": mime_type}}
    )

# Get stored image bytes for a product
def get_product_image_data(product_id):
    client = get_mongo_client()
    db = client["shop"]
    return db.products.find_one({"product_id": product_id}, {"_id": 0, "image_data": 1, "image_mime": 1})

# Compute dynamic average ratings and review counts via MongoDB aggregation pipeline
def get_products_with_ratings(category=None, q=None, min_rating=None, limit=100, product_ids=None, min_price=None, max_price=None, sort_dir=1):
    client = get_mongo_client()
    db = client["shop"]
    pipeline = []
    match_filter = {}
    if product_ids is not None:
        match_filter["product_id"] = {"$in": product_ids}
    if category and category != "All":
        match_filter["category"] = category
    if q:
        match_filter["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]
    price_cond = {}
    if min_price is not None: price_cond["$gte"] = float(min_price)
    if max_price is not None: price_cond["$lte"] = float(max_price)
    if price_cond:
        match_filter["price"] = price_cond
    if match_filter:
        pipeline.append({"$match": match_filter})
    pipeline.append({"$unwind": {"path": "$reviews", "preserveNullAndEmptyArrays": True}})
    pipeline.append({
        "$group": {
            "_id": "$product_id",
            "product_id": {"$first": "$product_id"},
            "name": {"$first": "$name"},
            "category": {"$first": "$category"},
            "price": {"$first": "$price"},
            "description": {"$first": "$description"},
            "attributes": {"$first": "$attributes"},
            "image_url": {"$first": "$image_url"},
            "avg_rating": {"$avg": "$reviews.rating"},
            "review_count": {"$sum": {"$cond": [{"$gt": ["$reviews.rating", 0]}, 1, 0]}}
        }
    })
    if min_rating is not None and float(min_rating) > 0:
        pipeline.append({"$match": {"avg_rating": {"$gte": float(min_rating)}}})
    pipeline.append({
        "$project": {
            "_id": 0,
            "product_id": 1,
            "name": 1,
            "category": 1,
            "price": 1,
            "description": 1,
            "attributes": 1,
            "image_url": 1,
            "avg_rating": {"$round": [{"$ifNull": ["$avg_rating", 0.0]}, 1]},
            "review_count": 1
        }
    })
    pipeline.append({"$sort": {"price": sort_dir}})
    pipeline.append({"$limit": limit})
    return list(db.products.aggregate(pipeline))

aggregate_product_ratings = get_products_with_ratings

# Compute category counts and price distribution buckets in a single roundtrip via $facet
def get_catalog_facets():
    client = get_mongo_client()
    db = client["shop"]
    pipeline = [{
        "$facet": {
            "categories": [{"$sortByCount": "$category"}],
            "price_buckets": [{
                "$bucket": {
                    "groupBy": "$price",
                    "boundaries": [0, 50, 200, 1000],
                    "default": "1000+",
                    "output": {"count": {"$sum": 1}}
                }
            }]
        }
    }]
    res = list(db.products.aggregate(pipeline))
    if not res:
        return {"categories": [], "price_buckets": []}
    facets = res[0]
    label_map = {0: "Under $50", 50: "$50-$200", 200: "$200-$1000", "1000+": "$1000+"}
    for b in facets.get("price_buckets", []):
        b["label"] = label_map.get(b["_id"], str(b["_id"]))
    return facets

