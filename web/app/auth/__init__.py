from flask import Blueprint

# Initalization of authentication blueprint.
auth = Blueprint('auth', __name__)

from . import views
