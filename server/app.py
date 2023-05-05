import yaml
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from db import db
from resources.book import bp


def create_app():
    config_file = os.path.join(
        os.path.dirname(__file__), 'config.yaml')
    with open(config_file, "r") as f:
        DB_CONFIG = yaml.load(f, Loader=yaml.FullLoader)

    # instantiate the app
    app = Flask(__name__)
    app.register_blueprint(bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'postgresql://{DB_CONFIG["username"]}:{DB_CONFIG["password"]}@'
        f'{DB_CONFIG["hostname"]}:{DB_CONFIG["port"]}/{DB_CONFIG["dbName"]}')

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
