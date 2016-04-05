from flask import render_template, url_for, redirect
from . import main
from .. import db
#from ..models import DB_MODEL_NAME
#from .forms import FORM_NAME


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
