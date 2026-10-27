from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Restaurant, FoodItem
from utils import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------- helpers ----------
def _bad_url(url):
    return bool(url) and not url.startswith(("http://", "https://"))


def parse_restaurant(form):
    """Validate the restaurant form. Returns (data, error)."""
    name = form.get("name", "").strip()
    cuisine = form.get("cuisine", "").strip()
    address = form.get("address", "").strip()
    image_url = form.get("image_url", "").strip()
    try:
        rating = float(form.get("rating") or 4.0)
        delivery_time = int(form.get("delivery_time") or 30)
    except ValueError:
        return None, "Rating and delivery time must be numbers."

    if not name or not cuisine or not address:
        return None, "Name, cuisine and address are required."
    if not 0 <= rating <= 5:
        return None, "Rating must be between 0 and 5."
    if not 5 <= delivery_time <= 180:
        return None, "Delivery time must be between 5 and 180 minutes."
    if _bad_url(image_url):
        return None, "Image link must start with http:// or https://"

    return {
        "name": name[:120], "cuisine": cuisine[:120], "address": address[:255],
        "image_url": image_url[:255] or None, "rating": rating,
        "delivery_time": delivery_time, "is_active": "is_active" in form,
    }, None


def parse_item(form):
    """Validate the menu item form. Returns (data, error)."""
    name = form.get("name", "").strip()
    description = form.get("description", "").strip()
    image_url = form.get("image_url", "").strip()
    try:
        price = Decimal(form.get("price", "").strip())
    except InvalidOperation:
        return None, "Price must be a number."

    if not name:
        return None, "Item name is required."
    if not (Decimal("0") < price <= Decimal("99999")):
        return None, "Price must be more than 0."
    if _bad_url(image_url):
        return None, "Image link must start with http:// or https://"

    return {
        "name": name[:120], "description": description[:255] or None,
        "price": price.quantize(Decimal("0.01")), "image_url": image_url[:255] or None,
        "is_veg": "is_veg" in form, "is_available": "is_available" in form,
    }, None


# ---------- restaurants ----------
@admin_bp.route("/")
@admin_required
def dashboard():
    restaurants = Restaurant.query.order_by(Restaurant.created_at.desc()).all()
    return render_template("admin/dashboard.html", restaurants=restaurants)


@admin_bp.route("/restaurants/new", methods=["GET", "POST"])
@admin_required
def restaurant_new():
    if request.method == "POST":
        data, error = parse_restaurant(request.form)
        if error:
            flash(error, "error")
            return render_template("admin/restaurant_form.html", r=request.form, title="Add restaurant")
        db.session.add(Restaurant(**data))
        db.session.commit()
        flash("Restaurant added. Now add its menu items.", "success")
        return redirect(url_for("admin.dashboard"))
    defaults = {"rating": 4.0, "delivery_time": 30, "is_active": True}
    return render_template("admin/restaurant_form.html", r=defaults, title="Add restaurant")


@admin_bp.route("/restaurants/<int:rid>/edit", methods=["GET", "POST"])
@admin_required
def restaurant_edit(rid):
    restaurant = db.get_or_404(Restaurant, rid)
    if request.method == "POST":
        data, error = parse_restaurant(request.form)
        if error:
            flash(error, "error")
            return render_template("admin/restaurant_form.html", r=request.form, title="Edit restaurant")
        for key, value in data.items():
            setattr(restaurant, key, value)
        db.session.commit()
        flash("Restaurant updated.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/restaurant_form.html", r=restaurant, title="Edit restaurant")


@admin_bp.route("/restaurants/<int:rid>/delete", methods=["POST"])
@admin_required
def restaurant_delete(rid):
    restaurant = db.get_or_404(Restaurant, rid)
    try:
        db.session.delete(restaurant)  # its menu items are deleted with it
        db.session.commit()
        flash("Restaurant deleted.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("This restaurant has orders, so it can't be deleted. Edit it and untick 'Visible to customers' instead.", "error")
    return redirect(url_for("admin.dashboard"))


# ---------- menu items ----------
@admin_bp.route("/restaurants/<int:rid>/items")
@admin_required
def items(rid):
    restaurant = db.get_or_404(Restaurant, rid)
    return render_template("admin/items.html", restaurant=restaurant)


@admin_bp.route("/restaurants/<int:rid>/items/new", methods=["GET", "POST"])
@admin_required
def item_new(rid):
    restaurant = db.get_or_404(Restaurant, rid)
    if request.method == "POST":
        data, error = parse_item(request.form)
        if error:
            flash(error, "error")
            return render_template("admin/item_form.html", restaurant=restaurant, i=request.form, title="Add menu item")
        db.session.add(FoodItem(restaurant_id=rid, **data))
        db.session.commit()
        flash("Menu item added.", "success")
        return redirect(url_for("admin.items", rid=rid))
    defaults = {"is_veg": True, "is_available": True}
    return render_template("admin/item_form.html", restaurant=restaurant, i=defaults, title="Add menu item")


@admin_bp.route("/restaurants/<int:rid>/items/<int:iid>/edit", methods=["GET", "POST"])
@admin_required
def item_edit(rid, iid):
    restaurant = db.get_or_404(Restaurant, rid)
    item = db.get_or_404(FoodItem, iid)
    if item.restaurant_id != rid:
        return redirect(url_for("admin.items", rid=rid))
    if request.method == "POST":
        data, error = parse_item(request.form)
        if error:
            flash(error, "error")
            return render_template("admin/item_form.html", restaurant=restaurant, i=request.form, title="Edit menu item")
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        flash("Menu item updated.", "success")
        return redirect(url_for("admin.items", rid=rid))
    return render_template("admin/item_form.html", restaurant=restaurant, i=item, title="Edit menu item")


@admin_bp.route("/restaurants/<int:rid>/items/<int:iid>/delete", methods=["POST"])
@admin_required
def item_delete(rid, iid):
    item = db.get_or_404(FoodItem, iid)
    if item.restaurant_id == rid:
        db.session.delete(item)
        db.session.commit()
        flash("Menu item deleted.", "success")
    return redirect(url_for("admin.items", rid=rid))
