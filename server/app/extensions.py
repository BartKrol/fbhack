# -*- coding: utf-8 -*-
"""Flask extensions --- initialised later in app.py"""

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask.ext.migrate import Migrate

migrate = Migrate()

from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

