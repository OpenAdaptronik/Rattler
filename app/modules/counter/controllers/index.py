from flask import render_template
from app.modules.counter import module_counter
from app.models.counter import Counter

@module_counter.route('/')
def index():
    return render_template('counter.html', counter=Counter.query.all(), title='Counter')
