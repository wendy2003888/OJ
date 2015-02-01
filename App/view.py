from App import app, loginmng, db
from flask import url_for, render_template, request, redirect, g
from flask.ext.login import login_user,login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, EditForm, ProblemForm
from config import Useriderr, Passworderr, UserWrong, UserConflict, PasswordWrong
from models import User, Problem

@loginmng.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.before_request
def before_request():
  g.user = current_user
  if g.user.is_authenticated():
    g.url = url_for('Profile', userid = g.user.userid)

def get_error(form):
  error = None
  for field in form:
    if field.errors:
      error = field.errors[0]
      break
  return error


@app.route('/')
def Homepage():
  # user = g.user
  return render_template('homepage.html')

@app.route('/<userid>/')
def Profile(userid):
  return render_template('profile.html')

@app.route('/<userid>/modify', methods = ['GET', 'POST'])
def Modify(userid):
  form = EditForm()
  user = User.query.get(userid)
  if request.method == 'POST':
    print form.nickname.data, form.password.data, form.email.data +'AAAA'
    if form.nickname.data == '':
      form.nickname.data = user.nickname 
    if form.password.data == '':
      form.password.data = user.password
    print form.nickname.data, form.password.data, form.email.data
    User.query.filter_by(userid = userid).update({'nickname': form.nickname.data, 
      'password': form.password.data, 
      'email': form.email.data})
    db.session.commit()
    return redirect(url_for('Profile', userid = userid))
  else:
    return render_template('modify.html',form=form, user = user)

@app.route('/administrater')
def Admin():
  return render_template('administrater.html')

@app.route('/problems/')
def Problems():
  problemlist = Problem.query.all()
  for p in problemlist:
    print p.title
  return render_template('problems.html', problemlist = problemlist)

@app.route('/addprb', methods = ['GET', 'POST'])
def Addprb():
  form = ProblemForm()
  if request.method == 'GET':
    return render_template('addprb.html', form = form)
  if request.method == 'POST' and form.validate():
    problem = Problem(form.title.data, form.description.data, 
      form.pbinput.data, form.pboutput.data, 
      form.sinput.data, form.soutput.data, form.hint.data)
    problem.save()
    return redirect(url_for('Problems'))
  error = get_error(form)
  return render_template('addprb.html', form = form, error = error)



@app.route('/login', methods = ['GET', 'POST'])
def Login():
  form = LoginForm()
  if request.method == 'GET':
    return render_template('login.html', form = form)
  else:
    if g.user is not None and g.user.is_authenticated():
      return redirect(url_for('Homepage'))
    elif form.validate_on_submit() :
      user = User.query.filter_by(userid = form.userid.data).first()
      if user == None:
        error = UserWrong
        return render_template('login.html', form = form, error = error)
      elif user.password != form.password.data:
        error = PasswordWrong
        return render_template('login.html', form = form, error = error)
      else:
        login_user(user)
        return redirect('/')

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('Homepage'))

@app.route("/sign_up", methods = ['GET', 'POST'])
def Sign_up():
  form = RegisterForm()
  if request.method == 'POST' and form.validate() :
    user = User(form.userid.data, form.password.data)
    user.save()
    login_user(user)
    return redirect(url_for('Homepage'))
  elif request.method == 'GET':
      return render_template('sign_up.html',form=form)
  else:
      error = get_error(form)
      return render_template('sign_up.html',form=form, error = error)



