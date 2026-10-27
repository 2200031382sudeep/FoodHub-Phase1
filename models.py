from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")  # customer | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    cuisine = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    rating = db.Column(db.Float, default=4.0)
    delivery_time = db.Column(db.Integer, default=30)  # minutes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("FoodItem", backref="restaurant", cascade="all, delete-orphan")


class FoodItem(db.Model):
    __tablename__ = "food_items"
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Numeric(8, 2), nullable=False)
    image_url = db.Column(db.String(255))
    is_veg = db.Column(db.Boolean, default=True)
    is_available = db.Column(db.Boolean, default=True)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Placed")
    delivery_address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="orders")
    restaurant = db.relationship("Restaurant")
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_items.id", ondelete="SET NULL"))
    name = db.Column(db.String(120), nullable=False)    # copy, so old orders never change
    price = db.Column(db.Numeric(8, 2), nullable=False)  # copy of the price at order time
    quantity = db.Column(db.Integer, nullable=False)
