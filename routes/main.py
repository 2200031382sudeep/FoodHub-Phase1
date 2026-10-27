from flask import Blueprint, render_template, abort
from extensions import db
from models import Restaurant
from utils import current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/restaurant/<int:rid>")
def restaurant(rid):
    r = db.get_or_404(Restaurant, rid)
    user = current_user()
    if not r.is_active and not (user and user.is_admin):
        abort(404)
    return render_template("restaurant.html", r=r)
