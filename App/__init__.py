from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


FLASKS_ETTINGS = 'config.py'

app = Flask(__name__)
app.config.from_pyfile(FLASKS_ETTINGS, silent = True)
db = SQLAlchemy(app)

