# phase2_check_db.py
import sqlite3
import json
import os

# Database file path
DB_PATH = "foodie.db"

def connect_db(db_path):
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' does not exist. Run Phase 1 setup first.")
        return None
    try:
        conn = sqlite3.connect(db_path)
        print("Connected to database successfully!")
        return conn
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return None

def check_products(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        print(f"Total products: {len(products)}")
        for p in products:
            print(p)
    except sqlite3.OperationalError as e:
        print("Error fetching products. Make sure the 'products' table exists.")
        print(e)

def check_users(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(f"\nTotal users: {len(users)}")
        for u in users:
            print(u)
    except sqlite3.OperationalError as e:
        print("Error fetching users. Make sure the 'users' table exists.")
        print(e)

def main():
    conn = connect_db(DB_PATH)
    if conn:
        check_products(conn)
        check_users(conn)
        conn.close()
        print("\nPhase 2 check completed!")

if __name__ == "__main__":
    main()
