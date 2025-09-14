# phase1_setup.py
import sqlite3

DB_PATH = "foodie.db"

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Insert sample products
sample_products = [
    ("Burger", 120),
    ("Pizza", 250),
    ("Sandwich", 100),
    ("Pasta", 180)
]

cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_products)

conn.commit()
conn.close()

print("Phase 1 setup complete. Products table created with sample data!")
