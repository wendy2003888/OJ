from App import db

class User(db.Model):
    id = db.Column(db.Integer)
    userid = db.Column(db.String(20), primary_key = True, unique = True)
    nickname = db.Column(db.String(20))
    password = db.Column(db.String(20), index = True, unique = True)
    role = db.Column(db.Boolean)
    email = db.Column(db.String(100), unique = True)



    def __init__(self, userid, password, role = False):
        self.userid = userid
        self.nickname = userid
        self.password = password
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
        
    def get_id(self):
        return unicode(self.userid)

    def is_admin(self):
        return self.role

    # def dis(self):
    #     print self.userid, self.password

    def __repr__(self):
        return '<User %s>' % (self.userid)


