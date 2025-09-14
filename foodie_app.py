# foodie_app.py
import streamlit as st
import sqlite3
import random
import datetime

DB_PATH = "foodie.db"

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="FoodieBot",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Welcome to FoodieBot!")
st.markdown("Select products by category, add to cart, and checkout!")

# -----------------------------
# Database Setup Functions
# -----------------------------
def create_products_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL
    )
    """)
    conn.commit()

def generate_sample_products(n=30):
    categories = ["Burger", "Pizza", "Sandwich", "Pasta", "Salad", "Dessert"]
    products = []
    for i in range(1, n+1):
        category = random.choice(categories)
        name = f"{random.choice(['Spicy', 'Cheesy', 'Crispy', 'Classic'])} {category}"
        product_id = f"P{i:03d}"
        price = round(random.uniform(50, 300), 2)
        products.append((product_id, name, category, price))
    return products

def insert_products_if_empty(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products = generate_sample_products()
        cursor.executemany(
            "INSERT INTO products (product_id, name, category, price) VALUES (?, ?, ?, ?)", products
        )
        conn.commit()

# -----------------------------
# Initialize Database
# -----------------------------
conn = sqlite3.connect(DB_PATH)
create_products_table(conn)
insert_products_if_empty(conn)

# -----------------------------
# Initialize Session State for Cart
# -----------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# -----------------------------
# Interactive Product Selection
# -----------------------------
st.subheader("🍽️ Available Products by Category")
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT category FROM products")
categories = [row[0] for row in cursor.fetchall()]

selected_category = st.selectbox("Select Category", categories)

cursor.execute("SELECT product_id, name, price FROM products WHERE category=?", (selected_category,))
products_in_category = cursor.fetchall()

if products_in_category:
    product_options = {f"{p[1]} - ₹{p[2]}": (p[0], p[2]) for p in products_in_category}
    selected_product_display = st.selectbox("Select Product", list(product_options.keys()))
    selected_product_id, selected_product_price = product_options[selected_product_display]

    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)

    if st.button("➕ Add to Cart"):
        if selected_product_id in st.session_state.cart:
            st.session_state.cart[selected_product_id]["quantity"] += quantity
        else:
            st.session_state.cart[selected_product_id] = {
                "name": selected_product_display,
                "price": selected_product_price,
                "quantity": quantity
            }
        st.success(f"Added {quantity} x {selected_product_display} to cart!")

else:
    st.info("No products available in this category.")

# -----------------------------
# Display Cart
# -----------------------------
st.subheader("🛒 Your Cart")
if st.session_state.cart:
    total_price = 0
    for item_id, item in st.session_state.cart.items():
        st.write(f"{item['name']} | Qty: {item['quantity']} | ₹{item['price'] * item['quantity']}")
        total_price += item['price'] * item['quantity']

    st.markdown(f"**Total: ₹{total_price}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Checkout"):
            st.success(f"Order placed! Total amount: ₹{total_price}")
            
            # Save order to database
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                quantity INTEGER,
                price REAL,
                total REAL,
                order_time TEXT,
                status TEXT
            )
            """)
            
            order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for item_id, item in st.session_state.cart.items():
                cursor.execute("""
                INSERT INTO orders (product_name, quantity, price, total, order_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    item['name'], item['quantity'], item['price'], item['price']*item['quantity'], order_time, "Pending"
                ))
            conn.commit()
            st.session_state.cart.clear()

    with col2:
        if st.button("🗑️ Clear Cart"):
            st.session_state.cart.clear()
            st.info("Cart cleared!")
else:
    st.info("Your cart is empty.")

conn.close()
