from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes import inventory_bp
    app.register_blueprint(inventory_bp)

    @app.route("/")
    def index():
        return {"message": "Inventory Management API is running"}, 200

    return app
