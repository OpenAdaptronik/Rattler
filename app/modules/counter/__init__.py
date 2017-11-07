from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

module_counter = Blueprint('counter', __name__, template_folder='scripts')

import app.modules.counter.controllers
