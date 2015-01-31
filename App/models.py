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
    
    def is_admin(self):
        return self.role

    def get_id(self):
        return unicode(self.userid)


    # def dis(self):
    #     print self.userid, self.password

    def __repr__(self):
        return '<User %s>' % (self.userid)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    title = db.Column(db.String(300))
    description = db.Column(db.String(9999))
    pbinput = db.Column(db.String(9999))
    pboutput = db.Column(db.String(9999))
    sinput = db.Column(db.String(9999))
    soutput = db.Column(db.String(9999))
    hint = db.Column(db.String(9999))

    def __init__(self, title, description, pbinput, pboutput, sinput, soutput, hint):
        self.title = title
        self.description = description
        self.pbinput = pbinput
        self.pboutput = pboutput
        self.sinput = sinput
        self.soutput = soutput
        self.hint = hint