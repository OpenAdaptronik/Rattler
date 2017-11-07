from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

default = Blueprint('default', __name__, template_folder='scripts')

@default.route('/')
def show():
    try:
        return render_template('index.html', title='home')
    except TemplateNotFound:
        abort(404)