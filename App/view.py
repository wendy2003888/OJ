from App import app, loginmng
from flask import url_for, render_template, request, redirect
from flask.ext.login import login_user,login_required, current_user
from forms import RegisterForm, LoginForm
from config import Useriderr, Passworderr
from models import User 

@loginmng.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/')
def Homepage():
	return render_template('homepage.html')

@app.route('/login', methods = ['GET', 'POST'])
def Login():
  form = LoginForm()
  if request.method == 'GET':
    return render_template('login.html', form = form)
  else:
    return redirect('/')
  # if form.validate_on_submit() :
  #   user = User.query.filter_by(userid = form.userid.data).first()
  #   if user.password != form.password.data:
  #     return 'Passworderror!'
  #   login_user(user)
  #   return 'Login Successfully!'

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



