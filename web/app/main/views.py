from . import main
from .. import db
from flask import render_template, url_for, redirect
from flask.ext.login import login_required
# from ..models import Model
# from .forms import Form


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')

@main.route('/base-schedule', methods=['GET', 'POST'])
@login_required
def base_schedule():
    return render_template('main/base_schedule.html')
