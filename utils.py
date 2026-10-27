from functools import wraps
from flask import session, redirect, url_for, flash, request, g, abort
from extensions import db
from models import User


def current_user():
    """Returns the logged-in User, or None."""
    if "user" not in g:
        uid = session.get("user_id")
        g.user = db.session.get(User, uid) if uid else None
    return g.user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user:
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login", next=request.path))
        if not user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped
