# phase3_setup_app.py
import sqlite3
import os

DB_PATH = "foodie.db"

def connect_db(db_path):
    if not os.path.exists(db_path):
        print(f"❌ Database file '{db_path}' does not exist. Run Phase 1 and 2 first.")
        return None
    try:
        conn = sqlite3.connect(db_path)
        print("✅ Connected to database successfully!\n")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def create_config_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    print("✅ 'app_config' table checked/created.")

def preload_default_data(conn):
    cursor = conn.cursor()
    default_settings = [
        ("app_name", "FoodieBot"),
        ("version", "1.0"),
        ("max_cart_items", "10")
    ]
    for key, value in default_settings:
        cursor.execute("""
            INSERT OR IGNORE INTO app_config (key, value) VALUES (?, ?)
        """, (key, value))
    conn.commit()
    print("✅ Default app configuration data loaded.")

def check_table_data(conn, table_name):
    cursor = conn.cursor()
    if not table_exists(conn, table_name):
        print(f"⚠️ Table '{table_name}' does not exist!")
        return False
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    if count == 0:
        print(f"⚠️ Table '{table_name}' exists but has no data!")
        return False
    print(f"✅ Table '{table_name}' has {count} record(s).")
    return True

def main():
    conn = connect_db(DB_PATH)
    if conn:
        # Setup
        create_config_table(conn)
        preload_default_data(conn)
        
        # Sanity checks
        print("\n🔹 Performing database sanity checks...")
        products_ok = check_table_data(conn, "products")
        users_ok = check_table_data(conn, "users")
        
        if products_ok and users_ok:
            print("\n🎯 Phase 3 completed! Database is ready for the app.")
        else:
            print("\n⚠️ Phase 3 completed with warnings. Fix missing tables/data before running the app.")
        
        conn.close()

if __name__ == "__main__":
    main()

