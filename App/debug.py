#from config import SQLALCHEMY_MIGRATE_REPO
from App import db
from forms import RegisterForm
from models import User	
import os.path


form = RegisterForm()

u = User(userid='aaabb1', password ='aaabb1')
db.session.add(u)
db.session.commit()

users = models.User.query.all()
print users