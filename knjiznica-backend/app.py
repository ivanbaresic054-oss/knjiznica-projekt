from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Učitavanje modela
    import models

    # Učitavanje ruta
    from routes import api
    app.register_blueprint(api)

    @app.route("/")
    def home():
        return {
            "poruka": "Knjiznica API radi"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)