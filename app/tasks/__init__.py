import rattler
from functools import wraps
from docopt import docopt

OPTIONS = docopt(rattler.__doc__, help=True, version='Rattler 1.0')

def command(func):
    @wraps(func)
    def wrapped():
        return func()

    # Register chosen function.
    if func.__name__ not in OPTIONS:
        raise KeyError('Cannot register {}, not mentioned in docstring/docopt.'.format(func.__name__))
    if OPTIONS[func.__name__]:
        command.chosen = func

    return wrapped

import app.tasks.init_db
import app.tasks.migrate_db
import app.tasks.run