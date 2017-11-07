#!flask/bin/python
"""Rattler.

Usage:
  rattler.py init_db
  rattler.py migrate_db
  rattler.py run
  rattler.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Import tasks and run
import app.tasks
if __name__ == '__main__':
    getattr( app.tasks.command, 'chosen')()

