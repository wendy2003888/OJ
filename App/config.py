import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

ADMIN = 'admin'
ADMINKEY = 123456

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

UserConflict = 'UserID has been registed.'
Useriderr = 'UserID invalid. It can only contain NUMBERs & LETTERs, and length must be 6 to 20.'
Passworderr = 'Password invalid. It can only contain NUMBERs & LETTERs, and length must be 6 to 20.'


UserWrong = 'UserID dose not exist.'
PasswordWrong = 'Password is incorrect.'


Titleerr = 'Title can'