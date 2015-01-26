from App import db

Role_user = 0
Role_admin = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.String(22), index = True, unique = True)
    password = db.Column(db.String(100), index = True, unique = True)
    #role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

    def __repr__(self):
        return '<User %s>' % (self.userid)

    def save(self):
        db.session.add(self)
        db.session.commit()
    def dis(self):
        print self.userid, self.password

