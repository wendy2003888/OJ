import os

basedir = os.path.abspath(os.path.dirname(__file__) )
SQLALCHEMY_DATAVASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

Useriderr = 'UserID invalid. It can only contain NUMBERs & LETTERs, and length must be 6 to 20.'
Passworderr = 'Password invalid. It can only contain NUMBERs & LETTERs, and length must be 6 to 20.'

