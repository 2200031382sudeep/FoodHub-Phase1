def register_blueprints(app):
    """Each phase adds its blueprint here."""
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
