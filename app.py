from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from resource import *
from database.models import *
from config import *


def create_app(config_name = "Config"):
    app = Flask(__name__, static_folder="static")
    config_class = globals().get(config_name, Config)
    app.config.from_object(config_class)
    api = Api(app)
    Swagger(app)
    Bootstrap(app)
    CORS(app)
    reg_resources(api)
    app.register_blueprint(api_bp)

    @app.before_request
    def _db_connect():
        if db.is_closed():
            db.connect()

    @app.teardown_request
    def _db_close(exc):
        if not db.is_closed():
            db.close()

    with app.app_context():
        init_db()

    return app


if __name__ == "__main__":      #pragma: no cover
    flask_app = create_app()
    flask_app.run(host='localhost', port=5000, debug=True)
