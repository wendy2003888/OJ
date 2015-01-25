# from flask_wtf import 
from wtforms import Form, TextField, BooleanField, PasswordField, validators
import re

class RegisterForm(Form):
	userid = TextField('Userid')
	password = PasswordField('Password', [
		validators.Length(min = 6, max = 20)
		] )
	confirm = PasswordField('Repassword', [validators.EqualTo('password', message = 'confirm must match to password')] )

	def validate_userid(self):
		return re.match(r'^[\w]{6,20}$', self.userid.data)

	def validate_password(self):
		return re.match(r'^[\w]{6,20}$', self.password.data)

	