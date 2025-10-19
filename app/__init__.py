from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import os

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)
    else:
        # allow DATABASE_URL to be set via env for flexibility
        database_url = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI=database_url,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

    db.init_app(app)
    ma.init_app(app)
    api = Api(app)

    # Health check endpoint for EBS
    @app.route('/')
    def health_check():
        return {
            'status': 'healthy',
            'service': 'Flask Blacklist API',
            'version': '1.0.0'
        }, 200

    # import resources here to register endpoints
    from .resources.blacklist import BlacklistResource, BlacklistLookupResource

    api.add_resource(BlacklistResource, '/blacklists')
    api.add_resource(BlacklistLookupResource, '/blacklists/<string:email>')

    # static bearer token for simplicity (can be overridden with env)
    app.config.setdefault('STATIC_BEARER_TOKEN', os.environ.get('STATIC_BEARER_TOKEN', 'secret-token'))

    # Create tables automatically on startup
    with app.app_context():
        db.create_all()

    return app
