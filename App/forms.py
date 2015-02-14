from flask_wtf import Form 
from wtforms import TextField, BooleanField, PasswordField, SelectField, validators
#from wtforms.validators import DataRequired, Length, EqualTo
import re


class RegisterForm(Form):
    userid= TextField('user ID', [
    	validators.Length(min = 3, max = 20, message="UserID's length must between 3 and 20.")
    	])
    password = PasswordField('PassWord', [
    	validators.Length(min = 6, max = 20, message='password length must between 6 and 20.')
    	])
    confirm = PasswordField('Repeat Password',[
    	validators.EqualTo('password',message = 'Password must match')
    	])

class LoginForm(Form):
	userid = TextField('user ID')
	password = PasswordField('PassWord')


class EditForm(Form):
	nickname = TextField('NickName', [
		validators.Length(max = 20, message='The max length of NickName should not over 20.')
		])
	password = PasswordField('PassWord', [
    	validators.Length(min = 6, max = 20, message='Password length must between 6 and 20.')
    	])
	confirm = PasswordField('Repeat Password',[
    	validators.EqualTo('password','Password must match')
    	])
	email = TextField('E-mail', [
    	validators.Length(max = 50, message='The max length of Email should not over 50.')
    	])

class ProblemForm(Form):
	title = TextField('Title', [
		validators.InputRequired(message = 'Title must not be None.'),
		validators.Length(max = 300, message = 'The max length of Title should not over 300.')
		])
	description = TextField('Description',[
		validators.length(max = 9999, message = 'The max length of description should not over 10000,')
		])
	pbinput = TextField('Input', [
		validators.InputRequired(message = 'Please enter problem input.'),
		validators.length(max = 9999, message = 'The max length of Input should not over 10000,')
		])
	pboutput = TextField('Output', [
		validators.InputRequired(message = 'Please enter problem output.'),
		validators.length(max = 9999, message = 'The max length  of Output should not over 10000,')
		])
	sinput = TextField('Sample Input',[
		validators.length(max = 9999, message = 'The max length of Sample Input should not over 10000,')
		])
	soutput = TextField('Sample Output',[
		validators.length(max = 9999, message = 'The max length should of Sample Output not over 10000,')
		])
	hint = TextField('Hint',[
		validators.length(max = 9999, message = 'The max length of Hint should not over 10000,')
		])
	timelmt = TextField('Time Limit',[
		validators.InputRequired(message = 'Please enter Time Limit.')
		])
	memorylmt = TextField('Memory Limit',[
		validators.InputRequired(message = 'Please enter Memory Limit.')
		])


class SubmitForm(Form):
	pbid = TextField('ProblemID', [
		validators.InputRequired(message = 'Problem, ID must not be None.')
		])
	language = SelectField('Language',choices = [('G++','G++'),('C++','C++'),('C','C'),('Python2.7','Python2.7')])
	code = TextField('Source Code',[
		validators.DataRequired( message = 'Source Code must not be None.')
		])

class DiscussForm(Form):
    title = TextField('Title',[
        validators.DataRequired( message = 'Please enter Title.')
        ])
    contents = TextField('Contents',[
        validators.DataRequired( message = 'Please enter Contents.')
        ])

class ReplyForm(Form):
    contents = TextField('Reply')