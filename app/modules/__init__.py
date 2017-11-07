from app import app
from app.modules import counter, default

app.register_blueprint(default.default, url_prefix='/')
app.register_blueprint(counter.module_counter, url_prefix='/counter')