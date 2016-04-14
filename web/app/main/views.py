from . import main
from .. import db
from flask import render_template, url_for, redirect
# from ..models import Model
# from .forms import Form


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
