import sqlite3
import os

print("🚀 Starting database check...")

# Check if database file exists
if not os.path.exists("foodie.db"):
    print("❌ foodie.db not found! Run phase1_setup_db.py first.")
    exit()

# Connect to the database
conn = sqlite3.connect("foodie.db")
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
table = cursor.fetchone()

if not table:
    print("❌ 'products' table not found! Run phase1_setup_db.py to create it.")
    conn.close()
    exit()

# Count products
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]
print(f"✅ Total products in database: {count}")

# Show 5 sample products
if count > 0:
    cursor.execute("SELECT product_id, name, category, price FROM products LIMIT 5")
    rows = cursor.fetchall()
    print("\n📌 Sample Products:")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | ${row[3]}")
else:
    print("⚠️ Database is empty! Run phase1_setup_db.py to insert products.")

conn.close()
