from App import db
from App.models import  User

db.drop_all()
db.create_all()

# tmp = User('w111111', 'w111111')
# tmp.save()
