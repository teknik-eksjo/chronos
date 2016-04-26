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
from .forms import AddTeacherForm, ExcelUploadForm
from ..models import User
from sqlalchemy import desc


@admin.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    """Main route for admin user interface.

    Administrator permissions is required to
    grant acess to this page.
    """
    return render_template('admin/admin.html')


@admin.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    teachers = User.query.filter_by(password_hash=None).order_by(User.first_name)
    return render_template('admin/users.html', teachers=teachers)


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = AddTeacherForm()

    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.users'))

    return render_template('admin/add.html', form=form)


@admin.route('/users/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_users():
    form = ExcelUploadForm()

    if form.validate_on_submit():
        pass

    return render_template('admin/upload.html', form=form)
