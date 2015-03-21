# -*- coding: utf-8 -*-
"""Flask extensions --- initialised later in app.py"""

# This one cannot be global
# from flask.ext.restful import Api
# api = Api()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()

