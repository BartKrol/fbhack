from flask import Flask
from settings.config import config
from .extensions import db, migrate, bootstrap


def create_app(config_name):
    """Create a flask app from a config"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    #print dir(app.config)
    register_extensions(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from preview import preview as preview_blueprint
    app.register_blueprint(preview_blueprint, url_prefix='/preview')

    # TODO - remove
    from . import models
    #app.run('0.0.0.0', debug=True, port=8100, ssl_context='adhoc')
    return app


def register_extensions(app):
    """Register flask extensions"""
    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)

