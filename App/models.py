from App import db

Role_user = 0
Role_admin = 1


class User(db.Model):
    id = db.Column(db.Integer)
    userid = db.Column(db.String(22), primary_key = True, unique = True)
    password = db.Column(db.String(100), index = True, unique = True)
    #role = db.Column(db.SmallInteger, default = Role_user)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anomymous(self):
        return False
        
    def get_id(self):
        return unicode(self.userid)


    # def dis(self):
    #     print self.userid, self.password

    def __repr__(self):
        return '<User %s>' % (self.userid)


