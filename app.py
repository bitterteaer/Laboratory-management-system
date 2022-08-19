from flask import g, Flask, url_for, redirect, request, render_template, session
from flask_migrate import Migrate
from exts import db
from decorations import login_required
from models import User
import config

from blueprints.user import bp as user_bp
from blueprints.device import bp as device_bp
from blueprints.data import bp as data_bp
from blueprints.register_requests import bp as register_requests_bp
from blueprints.big_data import bp as big_data_bp

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(device_bp)
app.register_blueprint(data_bp)
app.register_blueprint(register_requests_bp)
app.register_blueprint(big_data_bp)

migrate = Migrate(app, db)


@app.before_request
def before_request():
    id_user = session.get("id_user")
    if id_user:
        try:
            user = User.query.get(id_user)
            g.user = user
        except:
            g.user = None


@app.route("/")
@login_required
def index():
    return redirect(url_for('static', filename='layui/examples/layout-admin.html'))


if __name__ == '__main__':
    app.debug = True
    app.run()
