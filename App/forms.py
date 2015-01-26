from flask_wtf import Form 
from wtforms import TextField, BooleanField, PasswordField, validators
#from wtforms.validators import DataRequired, Length, EqualTo
import re


class RegisterForm(Form):
    userid= TextField('user ID', [validators.Length(min = 3, max = 20)] )
    password = PasswordField('PassWord', [
    	validators.Length(min = 6, max = 20)
    	])
    confirm = PasswordField('Repeat Password',[
    	validators.EqualTo('password','Password must match')
    	])

class LoginForm(Form):
	userid = TextField('user ID')
	password = PasswordField('PassWord')