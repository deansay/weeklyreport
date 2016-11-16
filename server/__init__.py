from flask import Flask

import config

app = Flask(__name__)
app.config.from_object(config)

from server.model.user import User
from server.model.task import Task
from server.model.report import Report


from server.model import db
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)


from server.api import login_handler, task_handler, user_handler
import server.api.task_handler
import server.api.user_handler



