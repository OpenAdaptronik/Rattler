from flask import render_template
from app.modules.counter import module_counter
from app.models.counter import Counter
from app import db

@module_counter.route('/sub/<int:id>')
def subAction(id):
    counter = Counter.query.get(id)
    counter.status -= 1 
    db.session.add(counter)
    db.session.commit()
    return render_template('counter.html', counter=Counter.query.all(), title='Counter++')
