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


@admin.route('/teachers', methods=['GET', 'POST'])
@login_required
@admin_required
def teachers():
    teachers = User.query.filter_by(password_hash=None).order_by(User.first_name)
    return render_template('admin/teachers.html', teachers=teachers)


@admin.route('/teachers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_teacher():
    form = AddTeacherForm()

    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.teachers'))

    return render_template('admin/add.html', form=form)


@admin.route('/teachers/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_teachers():
    form = ExcelUploadForm()

    if form.validate_on_submit():
        pass

    return render_template('admin/upload.html', form=form)
