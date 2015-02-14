from App import db

class User(db.Model):
    id = db.Column(db.Integer)
    userid = db.Column(db.String(20), primary_key = True, unique = True)
    nickname = db.Column(db.String(20))
    password = db.Column(db.String(20), index = True)
    role = db.Column(db.Boolean)
    email = db.Column(db.String(100), unique = True)
    accnt = db.Column(db.Integer, default = 0)
    submition = db.Column(db.Integer, default = 0)



    def __init__(self, userid, password, role = False):
        self.userid = userid
        self.nickname = userid
        self.password = password
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()
        # db.session.close()

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
    ratio = db.Column(db.Float, default = 0.0)
    accnt = db.Column(db.Integer, default = 0)
    submitcnt = db.Column(db.Integer, default = 0)
    timelmt = db.Column(db.Integer)
    memorylmt = db.Column(db.Integer)

    def __init__(self, title, description, pbinput, pboutput, sinput, soutput, hint, timelmt, memorylmt):
        self.title = title
        self.description = description
        self.pbinput = pbinput
        self.pboutput = pboutput
        self.sinput = sinput
        self.soutput = soutput
        self.hint = hint
        self.timelmt = timelmt
        self.memorylmt = memorylmt

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()


class Submit(db.Model):
    runid = db.Column(db.Integer, primary_key = True, unique = True)
    userid = db.Column(db.String(20))
    pbid = db.Column(db.Integer)
    code = db.Column(db.Text)
    result = db.Column(db.String(20), default = 'Pending')
    memory = db.Column(db.Integer, default = None)
    jgtime = db.Column(db.Integer, default = None)
    language = db.Column(db.String(20))
    codelen = db.Column(db.Integer)
    time = db.Column(db.String(20))
    memory_used = db.Column(db.Integer, default = None)
    time_used = db.Column(db.Integer, default = None)
    CEmsg = db.Column(db.Text, default = None)

    def __init__(self, runid, userid, pbid, code, language, time):
        self.runid = runid
        self.userid = userid
        self.pbid = pbid
        self.code = code
        self.language = language
        self.time = time
        self.codelen = len(self.code)


    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

class Forum(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    pbid = db.Column(db.Integer)
    userid = db.Column(db.String(22))
    title = db.Column(db.Text)
    contents = db.Column(db.Text)
    time = db.Column(db.String(20))

    def __init__(self, pbid, userid, title, contents, time):
        self.pbid = pbid
        self.userid = userid
        self.title = title
        self.contents = contents
        self.time = time

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cid = db.Column(db.Integer)
    userid = db.Column(db.String(22))
    contents = db.Column(db.Text)
    time = db.Column(db.String(20))

    def __init__(self, cid, userid, contents, time):
        self.cid = cid
        self.userid = userid
        self.contents = contents
        self.time = time

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()
