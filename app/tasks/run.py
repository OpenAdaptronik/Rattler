from app.tasks import command
from app import app

@command
def run():
    app.run(debug=True, host='0.0.0.0')