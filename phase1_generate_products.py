import json
import random
print("🚀 Script started...")
categories = {
    "Burgers": ["classic", "fusion", "vegetarian"],
    "Pizza": ["traditional", "gourmet", "personal"],
    "Fried Chicken": ["wings", "tenders", "sandwiches"],
    "Tacos & Wraps": ["mexican", "fusion", "healthy"],
    "Sides & Appetizers": ["fries", "onion rings", "nuggets"],
    "Beverages": ["sodas", "shakes", "specialty drinks"],
    "Desserts": ["ice cream", "cookies", "pastries"],
    "Salads & Healthy Options": ["green", "protein", "low-carb"],
    "Breakfast Items": ["pancakes", "sandwiches", "omelettes"],
    "Limited Time Specials": ["festive", "fusion", "premium"]
}

def generate_products(n=100):
    products = []
    product_id = 1

    for category, subcats in categories.items():
        for _ in range(n // len(categories)):   # distribute products equally
            product = {
                "product_id": f"FF{product_id:03d}",
                "name": f"{random.choice(['Spicy','Cheesy','Crispy','Fusion','Classic'])} {random.choice(subcats).title()} {category[:-1]}",
                "category": category,
                "description": f"A delicious {category} with {random.choice(['fusion flavors','classic taste','unique toppings'])}",
                "ingredients": random.sample(["chicken","beef","cheese","lettuce","tomato","onion","jalapeno","mayo","bbq sauce","garlic bread"], 4),
                "price": round(random.uniform(5,20),2),
                "calories": random.randint(200,800),
                "prep_time": f"{random.randint(5,15)} mins",
                "dietary_tags": random.sample(["spicy","vegan","contains_gluten","low_calorie","fusion"], 2),
                "mood_tags": random.sample(["comfort","indulgent","adventurous","healthy","quick"], 2),
                "allergens": random.sample(["gluten","soy","dairy","nuts"], 2),
                "popularity_score": random.randint(50,100),
                "chef_special": random.choice([True, False]),
                "limited_time": random.choice([True, False]),
                "spice_level": random.randint(1,10),
                "image_prompt": f"Image of {category} with {random.choice(['cheese','spice','fusion style'])}"
            }
            products.append(product)
            product_id += 1
    return products

# Generate products
products = generate_products()

# Save to JSON file
with open("products.json", "w") as f:
    json.dump(products, f, indent=4)

print(f"✅ Generated {len(products)} products and saved to products.json")
