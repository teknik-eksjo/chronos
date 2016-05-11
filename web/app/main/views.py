from . import main
from .. import db
from flask import render_template, url_for, redirect
from flask.ext.login import login_required, request
from ..models import Workday, BaseSchedule
# from .forms import Form


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')


@main.route('/base-schedule', methods=['GET', 'POST'])
@login_required
def base_schedule():
    data = request.get_json()

    if data:
        print(data)
        # index = data['index']
        # start = data['values'][0]
        # lunch_start = data['values'][1]
        # lunch_end = data['values'][2]
        # end = data['values'][3]

    else:
        return render_template('main/base_schedule.html')

    return ''


@main.route('/deviations', methods=['GET', 'POST'])
@login_required
def deviations():
    data = request.get_json()

    if data:
        print(data)

    else:
        return render_template('main/deviations.html')

    return ''
