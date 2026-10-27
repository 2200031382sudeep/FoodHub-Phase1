from flask import Flask, render_template, jsonify
from sqlalchemy import text

from config import Config
from extensions import db, migrate
from routes import register_blueprints
from utils import current_user

# Food categories shown on the homepage.
# In Phase 10 the admin manages these, and they will load from the `categories` table.
HOME_CATEGORIES = [
    ("Pizza", "🍕"), ("Burgers", "🍔"), ("Biryani", "🍛"), ("Chinese", "🥡"),
    ("South Indian", "🥘"), ("Desserts", "🍰"), ("Healthy", "🥗"), ("Beverages", "🥤"),
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    import models  # noqa: F401  (so Flask-Migrate can see the tables)
    register_blueprints(app)

    @app.context_processor
    def inject_user():
        return {"current_user": current_user()}

    @app.route("/")
    def index():
        from models import Restaurant
        restaurants = (Restaurant.query.filter_by(is_active=True)
                       .order_by(Restaurant.created_at.desc()).all())
        return render_template("index.html", categories=HOME_CATEGORIES, restaurants=restaurants)

    @app.route("/health/db")
    def health_db():
        """Visit /health/db to check that Flask can talk to MySQL."""
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(status="ok", database="connected")
        except Exception as exc:
            return jsonify(status="error", message=str(exc)), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
