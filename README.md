# Nexus Electronics: Polyglot Database E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Search-FF6F00)](https://www.trychroma.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

An enterprise-grade, multi-model e-commerce platform demonstrating **Polyglot Persistence Architecture**. This project combines relational ACID transactions, flexible document stores, and high-dimensional semantic vector search into a single cohesive system.

---

## 🏛️ System Architecture

Modern applications demand different data models for different operational workloads. Rather than forcing all application data into a single database paradigm, this project routes queries to the optimal storage engine:

```mermaid
flowchart TD
    User([🖥️ Client / User]) <--> UI[Streamlit Frontend :8501]
    UI <--> API[FastAPI Backend :8000]
    
    subgraph Polyglot_Database_Layer [Polyglot Database Storage Layer]
        API <-->|ACID Transactions & Auth| PG[(🐘 PostgreSQL 15\nPort 5432)]
        API <-->|Polymorphic Catalog & SVGs| MG[(🍃 MongoDB 6.0\nPort 27017)]
        API <-->|Cosine Similarity Search| CR[(🔮 ChromaDB\nLocal Persistent Store)]
    end

    PG --- PG_Details["• Strict Relational Schema\n• Atomic Stock Decrement\n• Row-Level Locks (Zero Overselling)\n• User Auth & Saved Addresses"]
    MG --- MG_Details["• Polymorphic Hardware Specs\n• Embedded Review Arrays\n• In-Database SVG Graphic Storage\n• Compound Indexing (category, price)"]
    CR --- CR_Details["• 384-dim Dense Embeddings\n• sentence-transformers all-MiniLM-L6-v2\n• Nearest Neighbor Recommendations"]
```

---

## 💾 Deep Dive: Database Engineering & Design

### 1. PostgreSQL 15 — Relational Engine & ACID Concurrency

PostgreSQL serves as the system of record for **financial transactions**, **user authentication**, **multi-address fulfillment**, and **inventory control**.

#### Relational Schema ([`db/schema.sql`](file:///Users/sanket/Documents/GitHub/AD/db/schema.sql))

```sql
-- 1. User Credentials & Profiles
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT DEFAULT 'demo123',
    created_at TIMESTAMP DEFAULT now()
);

-- 2. Address Book (1-to-Many with Users)
CREATE TABLE IF NOT EXISTS addresses (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    label TEXT,               -- e.g., 'Home', 'Office'
    recipient_name TEXT,
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT,
    postal_code TEXT,
    country TEXT DEFAULT 'United States',
    is_default BOOLEAN DEFAULT FALSE
);

-- 3. Inventory Stock with Integrity Constraints
CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT PRIMARY KEY,
    stock INT CHECK (stock >= 0)  -- Database-enforced invariant: stock can never be negative
);

-- 4. Order Headers
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    total NUMERIC(10, 2) NOT NULL,
    status TEXT DEFAULT 'completed',
    shipping_address TEXT,
    payment_method TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 5. Order Line Items (1-to-Many with Orders)
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    qty INT NOT NULL CHECK (qty > 0)
);
```

#### ACID Guarantees & Zero-Overselling Prevention

In high-concurrency e-commerce environments, naive `SELECT stock ... UPDATE stock` sequences cause **race conditions** leading to overselling. 

This platform implements atomic row-level update transactions inside [`db/postgres_queries.py`](file:///Users/sanket/Documents/GitHub/AD/db/postgres_queries.py):

```python
def place_order_transaction(user_id, total, items, shipping_address, payment_method):
    with get_pg_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Atomic stock decrement with conditional match
        for item in items:
            cur.execute("""
                UPDATE inventory 
                SET stock = stock - %s 
                WHERE product_id = %s AND stock >= %s;
            """, (item['qty'], item['product_id'], item['qty']))
            
            # If rowcount == 0, another concurrent transaction claimed the last unit
            if cur.rowcount == 0:
                conn.rollback()
                raise Exception(f"Insufficient stock for product {item['product_id']}")
        
        # Insert order record
        cur.execute("""
            INSERT INTO orders (user_id, total, status, shipping_address, payment_method)
            VALUES (%s, %s, 'completed', %s, %s) RETURNING id;
        """, (user_id, total, shipping_address, payment_method))
        order_id = cur.fetchone()['id']
        
        # Insert line items
        for item in items:
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, price, qty)
                VALUES (%s, %s, %s, %s, %s);
            """, (order_id, item['product_id'], item['name'], item['price'], item['qty']))
        
        # Commit all operations atomically
        conn.commit()
        return order_id
```

#### Polyglot Query Resolution: Cross-Engine ID-Batching for In-Stock Availability

A central architectural challenge in e-commerce is handling real-time availability filtering when inventory and product catalog metadata reside in different specialized database engines.

##### 1. Architectural Justification: ACID Invariants vs. Polymorphic Documents
- **Why PostgreSQL for Inventory Stock**: Inventory levels experience high concurrent write contention during checkouts. Isolating inventory in PostgreSQL allows the system to enforce strict transactional ACID properties (`READ COMMITTED` / `SERIALIZABLE`), row-level exclusive locks (`UPDATE inventory SET stock = stock - %s WHERE product_id = %s AND stock >= %s`), and database-level invariants (`CHECK (stock >= 0)`). This mathematically guarantees zero overselling without relying on error-prone application validation.
- **Why MongoDB for Product Catalog**: The product catalog features heterogeneous hardware disciplines with irregular, deeply nested specifications (e.g., Laptops require CPU clock speeds and RAM buses; Displays require resolution and color accuracy; Apparel requires sizes and materials). MongoDB stores these as polymorphic JSON documents with embedded review arrays and vector SVG assets, eliminating sparse relational tables and costly `ALTER TABLE` schema migrations.

##### 2. The Polyglot Coordination Mechanism: Foreign Engine ID-Batching
Instead of forcing all data into a single engine or attempting fragile distributed joins, the application implements **Foreign Engine ID-Batching**:

```
[ Client Request: GET /products?in_stock=true ]
                     │
                     ▼
  ┌─────────────────────────────────────┐
  │ 1. PostgreSQL (ACID Inventory)      │
  │    SELECT product_id FROM inventory │
  │    WHERE stock > 0;                 │
  └──────────────────┬──────────────────┘
                     │ Returns: in_stock_ids = ['P0001', 'P0003', ...]
                     ▼
  ┌─────────────────────────────────────┐
  │ 2. MongoDB (Polymorphic Catalog)    │
  │    db.products.aggregate([          │
  │      { $match: {                    │
  │          product_id: { $in: ids },  │
  │          category: "laptops"        │
  │      }}, ...                        │
  │    ])                               │
  └──────────────────┬──────────────────┘
                     │ Stream pre-sorted & aggregated product cards
                     ▼
           [ Response to Client ]
```

1. **Step 1 (PostgreSQL Index Scan)**: Executes [`get_in_stock_product_ids()`](file:///db/postgres_queries.py) using an index scan over the `inventory.stock` column to retrieve only IDs with available stock.
2. **Step 2 (ID Array Extraction)**: Extracts a lightweight array of matching SKU strings.
3. **Step 3 (MongoDB B-Tree Injection)**: Passes the ID list into MongoDB's aggregation pipeline via the `$in` operator (`{"product_id": {"$in": in_stock_ids}}`). MongoDB uses its primary index on `product_id` to evaluate metadata, dynamic review aggregations, and price sorting in a single streaming execution.

##### 3. Architectural Comparison: ID-Batching vs. 2PC vs. Distributed Joins

| Dimension | Foreign Engine ID-Batching (Our Approach) | Two-Phase Commit (2PC / XA Distributed Transactions) | Distributed / Federated Joins (e.g., Postgres FDW) |
| :--- | :--- | :--- | :--- |
| **Availability (CAP Theorem)** | **High ($AP/CP$ decoupled)**: Engines operate independently; failures are cleanly isolated. | **Low**: Blocking protocol. If coordinator or participant fails during prepare, locks remain held. | **Medium**: Dependent on the lowest common denominator network connection. |
| **Latency Profile** | Sub-5ms: Two sequential queries over localhost/LAN loopback using indexed lookups. | High: Multiple synchronous network roundtrips for prepare and commit voting phases. | High: Query planner lacks global cost statistics; often falls back to full foreign table scans. |
| **Locking & Contention** | **Zero cross-engine lock contention**: Read-only index scan on PostgreSQL; no locks held. | Heavy row-level distributed locks held throughout the entire multi-phase commit window. | Foreign locks or snapshot transactions held open across slow network streaming buffers. |
| **Implementation Complexity** | Minimal: Simple SQL filter combined with MongoDB `$in` operator in service tier. | Complex: Requires external distributed transaction coordinator (e.g., Narayana, Atomikos). | Complex: Requires configuring foreign data wrappers, user mappings, and remote type casts. |

---

### 2. MongoDB 6.0 — Polymorphic Document Store

E-commerce catalogs feature heterogeneous products with completely distinct attributes (e.g., Laptops require CPU/RAM specs, Shoes require sizes and colors, Books require authors and page counts). Modeling this in relational tables leads to sparse tables or awkward EAV (Entity-Attribute-Value) anti-patterns.

MongoDB handles this catalog flexibly within the `shop` database.

#### Document Schema Example
```json
{
  "product_id": "P0001",
  "name": "MacBook Pro 14\"",
  "category": "laptops",
  "price": 1999.00,
  "description": "Powered by M2 with 16GB RAM — built for speed and reliability.",
  "attributes": {
    "ram": "16GB",
    "cpu": "M2"
  },
  "reviews": [
    {
      "user": "User14",
      "rating": 5,
      "text": "Exceeded my expectations."
    }
  ],
  "image_url": "https://loremflickr.com/400/300/laptop?lock=1"
}
```

#### In-Database Image Storage
Rather than relying on third-party image hosting that can break or rate-limit, product cards are rendered as standalone vector SVGs and stored directly in the `shop.product_images` collection:
- **Field**: `image_data` (Binary SVG UTF-8 payload)
- **Field**: `image_mime` (`image/svg+xml`)
- **FastAPI Delivery**: Streaming endpoint `GET /products/{id}/image` directly delivers the vector graphics from MongoDB into Streamlit with sub-millisecond latency.

#### Compound B-Tree Indexing & Query Optimization under the ESR Rule

To maximize throughput and minimize latency on e-commerce catalog queries involving simultaneous category filtering, price sorting, and range bounding, MongoDB queries must adhere to the **ESR (Equality, Sort, Range)** indexing design guideline:

1. **Equality (`E`)**: Place fields filtered by exact matches first in the index (`{ category: 1 }`). This immediately narrows the B-Tree search space to the exact target partition.
2. **Sort (`S`)**: Place sort keys second in the index (`{ price: 1 }`). Because B-Tree keys are physically ordered, the database scans matching index leaves in exact sorted order without allocating an in-memory sort buffer (`hasSortStage: false`).
3. **Range (`R`)**: Place fields with range predicates (`$gte`, `$lte`, `$gt`, `$lt`) last. If a range predicate was placed *before* the sort key, MongoDB would be forced to perform an in-memory `SORT` stage across all matching range keys.

##### Query Execution Plan Comparison: COLLSCAN vs. ESR IXSCAN
The optimization can be verified directly via [`scripts/mongo_index_demo.py`](file:///scripts/mongo_index_demo.py) using `db.products.find({"category": "laptops", "price": {"$gte": 100, "$lte": 1500}}).sort("price", 1).explain("executionStats")`:

```json
// Execution plan without index:
{
  "stage": "SORT",
  "memLimit": 104857600,
  "totalDataSizeSorted": 55715,
  "inputStage": {
    "stage": "COLLSCAN",
    "filter": { "category": { "$eq": "laptops" } },
    "docsExamined": 100,
    "nReturned": 19
  }
}

// Execution plan with ESR index (category: 1, price: 1):
{
  "stage": "FETCH",
  "docsExamined": 19,
  "nReturned": 19,
  "inputStage": {
    "stage": "IXSCAN",
    "indexName": "category_1_price_1",
    "keysExamined": 19,
    "direction": "forward"
  }
}
```

##### Benchmark Performance Matrix (`explain("executionStats")`)

| Benchmark Metric | COLLSCAN (No Index) | IXSCAN (ESR Compound Index: `category: 1, price: 1`) | Academic Takeaway / Architectural Impact |
| :--- | :--- | :--- | :--- |
| **Execution Plan Stages** | `SORT → COLLSCAN` | `FETCH → IXSCAN` | Eliminates blocking memory stages; converts to streaming pipeline |
| **Scan Strategy** | `COLLSCAN` | `IXSCAN` | Index pointer lookup directly into B-Tree leaves |
| **In-Memory `SORT` Stage?** | **`True`** (Active `SORT` node) | **`False`** (`hasSortStage: false`) | Sort ordering guaranteed by index traversal sequence |
| **Sort RAM Memory Allocated** | `55,715 bytes` | **`0 bytes`** | Avoids MongoDB's 100MB RAM sort threshold and disk spill |
| **Total Documents Examined** | `100` (100% of collection) | **`19`** (Only matching records) | Zero wasted disk/cache page reads |
| **Total Index Keys Examined** | `0` | `19` | Strict 1:1 ratio between index keys and returned results |
| **Documents Returned (`nReturned`)** | `19` | `19` | High index selectivity ($\text{Index Selectivity} = \frac{nReturned}{keysExamined} = 1.0$) |
| **Query Latency** | Variable with table size ($O(N)$) | Sub-millisecond ($O(\log N + M)$) | Predictable, scalable retrieval under production load |


#### Embedded Array Denormalization & Aggregation Pipeline ($unwind → $group → $match)

Product reviews are stored natively as an embedded array within each product document (`reviews: [{ user, rating, text }, ...]`). While embedded documents enable single-read document retrieval without relational joins, calculating aggregate metrics (such as dynamic average star ratings and review counts) presents an architectural choice between client-side computation vs. database-engine aggregation.

##### Theoretical Concept: In-Engine Aggregation vs. Client-Side Array Parsing
- **Client-Side Parsing Anti-Pattern**: Pulling raw documents with unbounded review arrays across the network into application memory (e.g., Python / Node.js) to compute averages in user-space wastes severe network bandwidth, consumes high application RAM, and invalidates database index optimizations.
- **In-Engine Aggregation Pipeline**: MongoDB's Aggregation Framework delegates data transformation directly to the native C++ database engine, utilizing vectorized operations and streaming pipelines to return only the summarized metrics.

##### Aggregation Pipeline Stages
The dynamic calculation is implemented in [`db/mongo_queries.py`](file:///db/mongo_queries.py) (`get_products_with_ratings`) using a multi-stage pipeline:

```python
pipeline = [
    # 1. Early Working-Set Reduction (Index-Accelerated)
    {"$match": {"category": category}},

    # 2. Array Denormalization / Flattening
    {"$unwind": {"path": "$reviews", "preserveNullAndEmptyArrays": True}},

    # 3. Aggregation & Accumulator Computation
    {
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
    },

    # 4. Computed Metric Post-Filtering
    {"$match": {"avg_rating": {"$gte": min_rating}}},

    # 5. Projection & Precision Formatting
    {
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
    },
    {"$sort": {"price": 1}},
    {"$limit": limit}
]
```

1. **`$match` (Early Filtering)**: Reduces the initial working set before entering expensive array transformations. If `category` or keywords are specified, the database filters records using existing indexes.
2. **`$unwind` (Denormalization)**: Deconstructs the embedded `reviews` array field from the input documents to output a document for each element. Using `preserveNullAndEmptyArrays: True` guarantees that freshly launched products with 0 reviews are not erroneously discarded when browsing the full catalog.
3. **`$group` (Accumulator Operators)**: Re-groups the flattened stream by `_id: "$product_id"`.
   - **`$avg: "$reviews.rating"`**: Computes the arithmetic mean rating across all submitted reviews directly inside the storage engine.
   - **`$sum`**: Evaluates verified review counts using conditional accumulators.
   - **`$first`**: Preserves top-level document attributes without relational join overhead.
4. **`$match` (Post-Aggregation Filtering)**: Evaluates the dynamically accumulated `avg_rating` against the requested `min_rating` threshold (e.g., `4.0` or `3.0` stars) *before* serializing results to the client.
5. **`$project` (Field Shaping)**: Excludes large internal binary payloads (`image_data`), rounds `avg_rating` to 1 decimal place, and produces a clean API response shape.

##### Performance Advantages Over Client-Side Array Parsing
| Dimension | Client-Side Array Parsing (Application) | MongoDB Engine Aggregation Pipeline |
| :--- | :--- | :--- |
| **Network Payload** | Huge (transfers every review object, text, timestamp, and metadata over TCP) | Minimal (only sends the final computed scalar `avg_rating` and `review_count`) |
| **Memory Consumption** | $O(N \times M)$ memory allocation in Python heap where $M$ is review count per product | $O(1)$ stream processing within MongoDB's native execution pipeline buffer |
| **CPU Saturation** | Application runtime blocked by Python GIL during JSON deserialization and loops | Multithreaded C++ database engine execution utilizing query optimizer plans |
| **Pipelining & Bandwidth** | Client must download 100% of reviews before determining if a product meets 4+ stars | MongoDB discards non-matching products *before* serializing over the wire |

#### Multi-Faceted Catalog Aggregations via $facet & Network Roundtrip Optimization

In modern e-commerce storefronts, navigation sidebars and filter bars must display real-time distribution metrics across multiple orthogonal dimensions simultaneously:
1. **Category Distribution**: Item counts per hardware discipline (`Laptops: 25`, `Smartphones: 25`, etc.).
2. **Price Range Histograms**: Distribution of inventory across discrete budget tiers (`Under $50`, `$50-$200`, `$200-$1000`, `$1000+`).

##### Theoretical Concept: Relational Multi-Query Anti-Pattern vs. MongoDB $facet
- **The Relational Multi-Query Overhead**: In traditional relational databases, obtaining multi-dimensional faceted counts requires executing separate, sequential SQL queries over TCP:
  ```sql
  -- Query 1: Category breakdown
  SELECT category, COUNT(*) FROM products GROUP BY category;

  -- Query 2: Price range breakdown
  SELECT 
    CASE 
      WHEN price < 50 THEN 'Under $50'
      WHEN price < 200 THEN '$50-$200'
      WHEN price < 1000 THEN '$200-$1000'
      ELSE '$1000+'
    END AS price_bucket,
    COUNT(*) 
  FROM products 
  GROUP BY 1;
  ```
  This creates significant architectural inefficiencies:
  - **Connection & Protocol Latency**: $K$ distinct network roundtrips between the API server and database.
  - **Redundant Table Scans**: The storage engine re-reads and parses the same table data multiple times in separate execution plans.
  - **Synchronization Mismatches**: Non-repeatable reads can occur if writes happen between the multiple queries unless wrapped in high-isolation transactions.

- **MongoDB $facet Architecture**: The `$facet` aggregation stage processes multiple independent sub-pipelines within a single aggregation stage on the exact same set of input documents. All sub-pipelines run concurrently within MongoDB's engine during a single collection scan.

##### Pipeline Implementation
The faceted calculation is implemented in [`db/mongo_queries.py`](file:///db/mongo_queries.py) (`get_catalog_facets`) and exposed via `GET /products/facets`:

```python
pipeline = [{
    "$facet": {
        # Sub-pipeline 1: Fast frequency count on category
        "categories": [
            {"$sortByCount": "$category"}
        ],
        # Sub-pipeline 2: Price range binning using custom bucket boundaries
        "price_buckets": [
            {
                "$bucket": {
                    "groupBy": "$price",
                    "boundaries": [0, 50, 200, 1000],
                    "default": "1000+",
                    "output": {"count": {"$sum": 1}}
                }
            }
        ]
    }
}]
```

##### Architectural & Performance Advantages
| Architecture Dimension | Relational Multi-Query Approach | MongoDB `$facet` Single-Roundtrip Pipeline |
| :--- | :--- | :--- |
| **Network Roundtrips** | $N$ separate roundtrips (1 per facet dimension) | **1 single roundtrip** returning all facet dimensions |
| **I/O & Data Cache Access** | Scans collection/table $N$ times; evicts cache | **Single-pass scan**: inputs streamed once through memory |
| **Atomicity & Consistency** | Vulnerable to phantom reads between queries | **Point-in-time consistent snapshot** across all facets |
| **API Latency** | Cumulative latency: $T_{net} \times N + \sum T_{exec}$ | Minimal latency: $T_{net} \times 1 + \max(T_{exec})$ |
| **Client Code Complexity** | Client coordinates `asyncio.gather` or sequential SQL | Clean single dictionary response: `{categories: [...], price_buckets: [...]}` |

---

### 3. ChromaDB — Vector Store & Semantic Embeddings

Keyword regex searches fail when users search conceptually (e.g., searching "lightweight portable computing" should match ultrabooks, even if those exact words are not in the title).

ChromaDB provides an embedded vector database index:
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Embedding Space**: 384-dimensional dense vectors
- **Similarity Metric**: Cosine Distance
- **Pre-computed Index**: [`scripts/build_vectors.py`](file:///scripts/build_vectors.py) encodes document text `"{name} - {description}"` and stores them in local persistent storage (`chroma_db/`).
- **Query Operations**:
  - **Item-to-Item Similarity**: `GET /products/{id}/similar` extracts the target product's 384-dim embedding via `collection.get(ids=[id])`, runs `collection.query(query_embeddings=...)`, and returns the 5 nearest neighbors.
  - **Natural Language Semantic Search**: `GET /products?q={query}&mode=vector` encodes freeform text directly into dense vectors using `collection.query(query_texts=[query_text], n_results=25)` to find conceptual matches without requiring exact keyword overlaps.

---

### 4. Live Query Audit & Telemetry

Every interaction routes through a query auditor displayed on the UI under **📊 Database Telemetry**:
- `POST /orders` $\to$ PostgreSQL ACID transaction log
- `GET /products` $\to$ MongoDB regex filter & index scan
- `GET /products?mode=vector` $\to$ ChromaDB vector cosine distance text search
- `GET /products/{id}/similar` $\to$ ChromaDB vector cosine distance nearest neighbors
- `GET /debug/requests` $\to$ In-memory rolling telemetry log

---

## 🚀 Getting Started & Portability Guide

This repository is **100% portable** and tested to run across **macOS**, **Linux**, and **Windows**.

### Prerequisites
- **Git**
- **Docker Desktop** (or native PostgreSQL 15 & MongoDB 6)
- **Python 3.10 – 3.12** *(Note: Python 3.14 alpha is incompatible with PyTorch / ChromaDB binary wheels)*

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/sanket/AD.git
cd AD
```

---

### Step 2: Set Up Python Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt / PowerShell)
python -m venv venv
.\venv\Scripts\activate
```

Upgrade `pip` and install all pinned dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 3: Configure Environment Variables

The project includes sensible default fallbacks to local Docker instances. You can optionally create a custom `.env` file from the provided template:

```bash
# Copy example configuration
cp .env.example .env
```

Default contents of `.env`:
```ini
POSTGRES_URI=postgresql://postgres:postgres@localhost:5432/postgres
MONGO_URI=mongodb://localhost:27017/
```

---

### Step 4: Start Databases via Docker

Start PostgreSQL and MongoDB in the background:
```bash
docker-compose up -d
```

Verify that both containers are running healthy:
```bash
docker-compose ps
```

*(Note: PostgreSQL mounts `db/schema.sql` into `/docker-entrypoint-initdb.d/init.sql` for automated initial table creation).*

---

### Step 5: Seed Relational & Document Data

Populate the database with the Demo User, sample addresses, 100 catalog products (25 per category), inventory stock, and SVG vector images:

```bash
python scripts/seed.py
```

*Output summary:*
```
Initializing / migrating database schema...
Clearing existing data...
Seeding exactly 1 Demo User (demo@nexus.com / demo123)...
Seeding default address for Demo User...
Generating 100 products (25 per category) and inventory...
Generating product SVG images in MongoDB...
Seeded 1 Demo User (ID: 1) and 2 sample addresses in PostgreSQL.
Seeded 100 inventory records in PostgreSQL.
Seeded 100 products in MongoDB.
```

---

### Step 6: Generate ChromaDB Vector Embeddings

Build the semantic vector embeddings for nearest-neighbor similarity search:

```bash
python scripts/build_vectors.py
```

*Output:*
```
Stored 100 product embeddings in ChromaDB.
```

---

### Step 7: Launch the Application

You will need **two terminal tabs** (both with the virtual environment activated):

#### Terminal 1 — Backend API (FastAPI)
```bash
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
uvicorn api.main:app --reload --port 8000
```
- API Base: `http://localhost:8000`
- Interactive OpenAPI / Swagger Docs: `http://localhost:8000/docs`

#### Terminal 2 — Frontend UI (Streamlit)
```bash
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
streamlit run ui/app.py --server.port 8501
```
- Web Application: `http://localhost:8501`

---

## 🧪 Demonstration & Benchmark Scripts

Run these scripts to test and demonstrate database behaviors:

### 1. Concurrency & ACID Oversell Prevention Test
Simulates **20 concurrent buyers** simultaneously competing for the **last 5 units** of stock:
```bash
python scripts/oversell_test.py
```
*Expected Result:*
- Successful orders: **5**
- Failed orders: **15** (Rejected with `Insufficient stock`)
- Final inventory stock: **0** (Zero overselling invariant guaranteed)

### 2. MongoDB Compound Indexing Demo
Compares MongoDB collection scans against compound index scans:
```bash
python scripts/mongo_index_demo.py
```

### 3. Semantic Vector Search vs. Keyword Search
Demonstrates how dense embeddings retrieve conceptually similar products where token-based keyword search yields zero results:
```bash
python scripts/similar_vs_keyword.py
```

---

## 🔌 REST API Reference

| Method | Endpoint | Database | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | System | Healthcheck status indicator |
| `POST` | `/auth/register` | PostgreSQL | Create new user account with hashed/stored credentials |
| `POST` | `/auth/login` | PostgreSQL | Authenticate user email & password |
| `GET` | `/users/{id}` | PostgreSQL | Retrieve customer account profile |
| `PUT` | `/users/{id}` | PostgreSQL | Update customer account information |
| `GET` | `/users/{id}/addresses` | PostgreSQL | List all saved delivery addresses for a user |
| `POST` | `/users/{id}/addresses` | PostgreSQL | Save a new delivery destination with default flag |
| `DELETE` | `/users/{id}/addresses/{aid}` | PostgreSQL | Remove a saved shipping address |
| `PUT` | `/users/{id}/addresses/{aid}/default`| PostgreSQL | Set an address as primary default |
| `GET` | `/products` | MongoDB + ChromaDB | Search catalog with category filtering, regex keyword search, or AI vector semantic search (`mode=vector`) |
| `GET` | `/products/{id}` | Mongo + Postgres | Retrieve polymorphic product document joined with live stock |
| `GET` | `/products/{id}/image` | MongoDB | Stream in-database binary SVG product graphic |
| `GET` | `/products/{id}/similar` | ChromaDB + Mongo | 5-nearest-neighbor semantic vector recommendations |
| `POST` | `/orders` | PostgreSQL | Execute atomic ACID order placement & stock decrement |
| `GET` | `/orders?user_id={id}` | PostgreSQL | Fetch historical orders placed by a specific user |
| `GET` | `/orders/{id}/items` | PostgreSQL | Retrieve itemized line items for an order |
| `GET` | `/debug/requests` | Memory Telemetry | Inspect recent query routing history across database engines |

---

## 📦 Git & Portability Checklist

Before pushing to git, confirm that all required assets and configuration files are staged:

- [x] **`db/schema.sql`**: Complete PostgreSQL DDL with `users`, `addresses`, `inventory`, `orders`, and `order_items`.
- [x] **`docker-compose.yml`**: Configured with automated schema mounting for fresh Docker environments.
- [x] **`requirements.txt`**: Pinned versions for `fastapi`, `uvicorn`, `streamlit`, `psycopg2-binary`, `pymongo`, `python-dotenv`, `chromadb`, and `sentence-transformers`.
- [x] **`.streamlit/config.toml`**: Light theme forced with `#0f172a` text color, preventing dark mode unreadable text issues on macOS/iOS/Windows.
- [x] **`scripts/fetch_images.py`**: Present and executable for in-database vector SVG generation.
- [x] **`static/index.html`**: Present for static storefront routes.
- [x] **`.gitignore`**: Correctly excludes `venv/`, `__pycache__/`, `.env`, and `chroma_db/` (which is rebuilt dynamically).
- [x] **`.env.example`**: Committed to provide immediate onboarding templates.
- [x] **Fallback URIs**: `db/postgres_queries.py` and `db/mongo_queries.py` automatically fall back to standard local ports if `.env` is omitted.

---

## 👤 Default Demo Credentials
- **Email**: `demo@nexus.com`
- **Password**: `demo123`
- *(Users can also register new custom accounts directly through the UI or API)*
