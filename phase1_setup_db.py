import sqlite3
import json
import os

print("🚀 Starting database setup...")

# Check if products.json exists
if not os.path.exists("products.json"):
    print("❌ products.json not found! Run phase1_generate_products.py first.")
    exit()

# Load generated products
with open("products.json") as f:
    products = json.load(f)

# Create database
conn = sqlite3.connect("foodie.db")
cursor = conn.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    description TEXT,
    ingredients TEXT,
    price REAL,
    calories INTEGER,
    prep_time TEXT,
    dietary_tags TEXT,
    mood_tags TEXT,
    allergens TEXT,
    popularity_score INTEGER,
    chef_special BOOLEAN,
    limited_time BOOLEAN,
    spice_level INTEGER,
    image_prompt TEXT
)
""")

# Insert products
for p in products:
    cursor.execute("""
    INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        p["product_id"], p["name"], p["category"], p["description"],
        ",".join(p["ingredients"]), p["price"], p["calories"], p["prep_time"],
        ",".join(p["dietary_tags"]), ",".join(p["mood_tags"]), ",".join(p["allergens"]),
        p["popularity_score"], p["chef_special"], p["limited_time"], p["spice_level"], p["image_prompt"]
    ))

conn.commit()

# Show confirmation
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]
print(f"✅ Inserted {count} products into foodie.db")

conn.close()
