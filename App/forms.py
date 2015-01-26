from flask_wtf import Form 
from wtforms import TextField, BooleanField, PasswordField
#from wtforms.validators import DataRequired, Length, EqualTo
import re


class RegisterForm(Form):
    userid= TextField('user ID')
    password = PasswordField('PassWord')
    confirm = PasswordField('Repeat Password')

    def validate_userid(self):
       return re.match(r'^[a-zA-Z0-9]{3,22}$',self.userid.data)

    def validate_password(self):
       return re.match(r'^[a-zA-Z0-9]{6,22}$',self.password.data)

    def validate_eq(self):
        return self.password.data == self.confirm.data
