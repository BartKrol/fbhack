from flask import Blueprint

preview = Blueprint('preview', __name__)

from . import views
