"""Adds 3 sample restaurants with menu items so you can see the app working.
Run once:  python seed_sample.py   (skips if restaurants already exist)"""
from decimal import Decimal
from app import app
from extensions import db
from models import Restaurant, FoodItem

SAMPLE = [
    ("Pizza Palace", "Pizza, Italian", "MG Road, Bengaluru", 4.4, 30, [
        ("Margherita Pizza", "Classic cheese and tomato", "199", True),
        ("Farmhouse Pizza", "Capsicum, onion, mushroom, corn", "299", True),
        ("Chicken Tikka Pizza", "Spicy chicken tikka topping", "349", False),
        ("Garlic Bread", "Toasted with butter and herbs", "129", True),
    ]),
    ("Biryani House", "Biryani, North Indian", "Indiranagar, Bengaluru", 4.6, 35, [
        ("Veg Biryani", "Fragrant rice with vegetables", "189", True),
        ("Chicken Dum Biryani", "Slow-cooked with spices", "279", False),
        ("Paneer Butter Masala", "Creamy tomato gravy", "239", True),
        ("Raita", "Cool curd with cucumber", "49", True),
    ]),
    ("Dragon Wok", "Chinese", "Koramangala, Bengaluru", 4.2, 28, [
        ("Veg Hakka Noodles", "Stir-fried with vegetables", "159", True),
        ("Chicken Fried Rice", "Wok-tossed with egg", "209", False),
        ("Gobi Manchurian", "Crispy cauliflower in sauce", "169", True),
        ("Spring Rolls", "Crunchy veg rolls (6 pcs)", "119", True),
    ]),
]

with app.app_context():
    if Restaurant.query.count():
        raise SystemExit("Restaurants already exist - nothing added.")
    for name, cuisine, address, rating, mins, items in SAMPLE:
        r = Restaurant(name=name, cuisine=cuisine, address=address, rating=rating, delivery_time=mins)
        for iname, desc, price, veg in items:
            r.items.append(FoodItem(name=iname, description=desc, price=Decimal(price), is_veg=veg))
        db.session.add(r)
    db.session.commit()
    print("Added 3 sample restaurants.")
