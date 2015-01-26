from App import app, db
from flask import url_for, render_template, request, redirect
from forms import RegisterForm	
from config import Useriderr, Passworderr
from models import User 



@app.route('/')
def Homepage():
	return render_template('homepage.html')

@app.route('/login')
def Login():
	return render_template('login.html')

@app.route("/sign_up", methods = ['GET', 'POST'])
def Sign_up():
  form = RegisterForm()
  if request.method == 'POST' and form.validate() :
    user = User(form.userid.data, form.password.data)
    user.save()
    return redirect('/')
  elif request.method == 'GET':
      return render_template('sign_up.html',form=form)
  else:
      return render_template('sign_up.html',form=form, error = 'Error')



