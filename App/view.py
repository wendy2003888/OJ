from flask import url_for, render_template, request, redirect
from App import app
from forms import RegisterForm
from models import User		
from config import Useriderr, Passworderr



@app.route('/')
def Homepage():
	return render_template('homepage.html')

@app.route('/login')
def Login():
	return render_template('login.html')

@app.route("/sign_up", methods = ['GET', 'POST'])
def Sign_up():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('sign_up.html',form=form)
    else:
        if not form.validate_userid():
        	error = Useriderr
        elif not form.validate_password():
        	error = Passworderr
       	elif not form.validate_eq():
       		error = 'Passwords must match'
       	else:
       		error = None
        if error:
        	return render_template('sign_up.html', form = form, error = error)
        else:
        	user = User(form.userid.data, form.password.data)
        	user.save()
        	return redirect('/')

