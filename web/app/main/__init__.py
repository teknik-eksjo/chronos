from flask import Blueprint

# Initialization of main blueprint.
main = Blueprint('main', __name__)

from . import views, errors
