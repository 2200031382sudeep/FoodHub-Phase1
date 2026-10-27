from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import User
from utils import current_user

auth_bp = Blueprint("auth", __name__)


def safe_next(target):
    """Only allow redirects to pages on our own site."""
    if target and target.startswith("/") and not target.startswith("//"):
        return target
    return url_for("index")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        error = None
        if len(name) < 2:
            error = "Please enter your name."
        elif "@" not in email or len(email) > 150:
            error = "Please enter a valid email."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif User.query.filter_by(email=email).first():
            error = "That email is already registered. Try logging in."

        if error:
            flash(error, "error")
            return render_template("auth/register.html", name=name, email=email)

        user = User(name=name, email=email)  # role defaults to "customer"
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session.clear()
        session["user_id"] = user.id
        flash(f"Welcome to FoodExpress, {user.name}!", "success")
        return redirect(url_for("index"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            flash("Logged in successfully.", "success")
            return redirect(safe_next(request.args.get("next")))

        flash("Wrong email or password.", "error")
        return render_template("auth/login.html", email=email)

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))
