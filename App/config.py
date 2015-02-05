import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
SQLALCHEMY_POOL_RECYCLE = 5
# SQLALCHEMY_POOL_TIMEOUT = 10


ITEMS_ON_PAGE = 50
ADMIN = 'admin'
ADMINKEY = 123456

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

UserConflict = 'UserID has been registed.'
Useriderr = 'UserID invalid. It can only contain NUMBERs & LETTERs, and length must be 6 to 20.'
Passworderr = 'Password invalid. It can only contain NUMBERs & LETTERs, and length must be 6 to 20.'


UserWrong = 'UserID dose not exist.'
PasswordWrong = 'Password is incorrect.'

Permissionerr = 'You are not authorized! Only admin are permitted.'