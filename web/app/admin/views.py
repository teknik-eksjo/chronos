from flask import (current_app,
                   flash,
                   redirect,
                   render_template,
                   request,
                   url_for)

from flask.ext.login import (login_user,
                             logout_user,
                             login_required,
                             current_user)

from . import admin
from .. import db
from ..decorators import admin_required, permission_required
from ..models import User


@admin.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    """Main route for admin user interface.

    Administrator permissions is required to
    grant acess to this page.
    """
    return 'Admin route.'
