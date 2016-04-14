from flask import Blueprint

# Initalization of admin blueprint.
admin = Blueprint('admin', __name__)

from . import views
