from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

FLASKS_ETTINGS = 'config.py'

app = Flask(__name__)
app.config.from_pyfile(FLASKS_ETTINGS, silent = True)
db = SQLAlchemy(app)

loginmng = LoginManager()

loginmng.setup_app(app)
#loginmng.login_view = '/login'