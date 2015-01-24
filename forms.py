from flask_wtf import Form, TextField, BooleanField, PasswordField
from flask_wtf import Required
import re

class RegisterForm(Form):
	userid = TextField('Userid', [validators.Required() ] )
	password = PasswordField('Password', [validators.Required() ] )

	def validate(self):
		if(re.match(r'^[\w]{6,20}$', self.userid.data) == None ):
			return False
		if(re.match(r'^[\w]{6,20}$', self.password.data) == None):
			return False
		return True

	