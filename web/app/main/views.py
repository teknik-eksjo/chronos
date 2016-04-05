from flask import render_template, url_for, redirect
from . import main
from .. import db
from ..models import Post
from .forms import PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
