from App import db
from App.models import  User
from App.config import ADMIN, ADMINKEY

db.drop_all()
db.create_all()

tmp = User(ADMIN, ADMINKEY, True)
tmp.save()
