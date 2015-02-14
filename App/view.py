from App import app, loginmng, db
from flask import url_for, render_template, request, redirect, g, flash
from flask.ext.login import login_user,login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, EditForm, ProblemForm, SubmitForm, DiscussForm, ReplyForm, InfoForm
from config import Useriderr, Passworderr, UserWrong, UserConflict, PasswordWrong, Permissionerr, ITEMS_ON_PAGE, POST_PER_PAGE
from models import User, Problem, Submit, Forum, Reply, Info
import time

@loginmng.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.before_request
def before_request():
  g.user = current_user
  if g.user.is_authenticated():
    g.url = url_for('Profile', userid = g.user.userid)
  info = Info.query.order_by(Info.id.desc()).first()
  g.info = info.contents


def get_error(form):
  error = None
  for field in form:
    if field.errors:
      error = field.errors[0]
      break
  return error

def get_time():
  return  time.strftime('%y-%m-%d %H:%M:%S')

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
    # print form.nickname.data, form.password.data, form.email.data +'AAAA'
    if form.nickname.data == '':
      form.nickname.data = user.nickname 
    if form.password.data == '':
      form.password.data = user.password
    # print form.nickname.data, form.password.data, form.email.data
    User.query.filter_by(userid = userid).update({'nickname': form.nickname.data, 
      'password': form.password.data, 
      'email': form.email.data})
    db.session.commit()
    return redirect(url_for('Profile', userid = userid))
  else:
    return render_template('modify.html',form=form, user = user)

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
    db.session.close()
    return redirect(url_for('Homepage'))
  elif request.method == 'GET':
      return render_template('sign_up.html',form=form)
  else:
      error = get_error(form)
      return render_template('sign_up.html',form=form, error = error)

@app.route('/administrater')
def Admin():
  return render_template('administrater.html')

@app.route('/problems/')
@app.route('/problems/page=<int:page>')
def Problems(page = 1):
  pbnum = Problem.query.count()
  pagenum = (pbnum - 1) / ITEMS_ON_PAGE + 1
  if g.user.is_admin():
    problemlist = Problem.query.paginate(page, ITEMS_ON_PAGE, False)
    for i in problemlist.items:
      print i.visible
  else:
    problemlist = Problem.query.filter_by(visible = True).paginate(page, ITEMS_ON_PAGE, False)
  return render_template('problems.html', problemlist = problemlist, page = page, pagenum = pagenum)

@app.route('/problems/<problemid>')
def Showprb(problemid):
  problem = Problem.query.get(problemid)
  #print problem
  return render_template('prbbase.html', problem = problem)

@app.route('/submit/<problemid>', methods=['GET','POST'])
@login_required
def Submits(problemid):
  form = SubmitForm()
  problem = Problem.query.get(problemid)
  if request.method == 'POST' and form.validate():
    submit = Submit(Submit.query.count() + 1 , g.user.userid, form.pbid.data,form.code.data, form.language.data, get_time() )
    submit.save()
    return redirect(url_for('Status', page =  1))
  error = get_error(form)
  return render_template('submit.html', form = form, problem = problem, error = error)

@app.route('/status/')
@app.route('/status/page=<int:page>')
def Status(page = 1):
  submit_list = Submit.query.order_by(Submit.runid.desc()).paginate(page, ITEMS_ON_PAGE, False)
  return render_template('status.html', submit_list = submit_list, page = page )

@app.route('/viewcode/rid=<runid>')
def Viewcode(runid):
  submit = Submit.query.filter_by(runid = runid).first()
  return render_template('viewcode.html', submit = submit)

@app.route("/show_compile_info/rid'='<runid>")
def Show_compile_info(runid):
  submit = Submit.query.get(runid)
  return render_template('show_CE_info.html', submit = submit)

@app.route('/ranklist/')
@app.route('/ranklist/<int:page>/')
def Ranklist(page = 1):
    user_list = User.query.order_by(User.accnt.desc(), User.submission, User.userid).paginate(page,ITEMS_ON_PAGE, False)
    return render_template('ranklist.html', page = page, user_list = user_list, strank = ITEMS_ON_PAGE * (page - 1) )


@app.route('/FAQ/')
def Faq():
  return render_template('faq.html')

@app.route('/discuss/pid=<pbid>', methods = ['GET', 'POST'])
@app.route('/discuss/pid=<pbid>?page=<int:page>', methods = ['GET', 'POST'])
def Discuss(pbid, page = 1):
  postlist = Forum.query.filter_by(pbid = pbid).order_by(Forum.id.desc()).paginate(page, POST_PER_PAGE, False)
  form = DiscussForm()
  if request.method == 'POST' and form.validate():
    forum = Forum(pbid, g.user.userid, form.title.data, form.contents.data, get_time())
    forum.save()
    return redirect(url_for('Discuss', pbid = pbid))
  return render_template('discuss.html', page = page, form = form, pbid = pbid, postlist = postlist)

@app.route('/comment/id=<cid>', methods = ['GET', 'POST'])
@app.route('/comment/id=<cid>?page=<int:page>', methods = ['GET', 'POST'])
def Show_comment(cid, page = 1):
  form = ReplyForm()
  comment = Forum.query.get(cid)
  replylist = Reply.query.filter_by(cid = cid).order_by(Reply.id.desc()).paginate(page, POST_PER_PAGE, False)
  if request.method == 'POST' and form.validate() :
    reply = Reply(cid, g.user.userid, form.contents.data, get_time())
    reply.save()
    return redirect(url_for('Show_comment', cid = cid))
  return render_template('show_comment.html', page = page, form = form, comment = comment, replylist = replylist)


@app.route('/manage/', methods = ['GET', 'POST'])
@login_required
def Manage():
  if not g.user.is_admin():
    flash(Permissionerr)
    return redirect(url_for('Profile', userid = g.user.userid))
  form = InfoForm()
  infolist = Info.query.order_by(Info.id.desc()).all()
  if request.method == 'POST' and form.validate() :
    info = Info(g.user.userid, form.contents.data, get_time())
    info.save()
    return redirect(url_for('Manage'))
  return render_template('manage.html', form = form, infolist = infolist)

@app.route('/delinfo/<iid>')
def Del_info(iid):
  Info.query.get(iid).delete()
  db.session.commit()
  db.session.close()
  return redirect( url_for('Manage') )

  

@app.route('/addprb/', methods = ['GET', 'POST'])
def Addprb():
  form = ProblemForm()
  if request.method == 'GET':
    return render_template('addprb.html', form = form)
  if request.method == 'POST' and form.validate():
    if form.visible.data == 'True':
      vis = True
    else:
      vis = False
    problem = Problem(form.title.data, form.description.data, 
      form.pbinput.data, form.pboutput.data, 
      form.sinput.data, form.soutput.data, form.hint.data,
      form.timelmt.data, form.memorylmt.data, vis ) 
    problem.save()
    return redirect(url_for('Problems', page = 1))
  error = get_error(form)
  return render_template('addprb.html', form = form, error = error)

@app.route('/editprb/<problemid>', methods = ['GET', 'POST'])
def Editprb(problemid):
  form = ProblemForm()
  pb = Problem.query.get(problemid)
  if request.method == 'GET':
    return render_template('editprb.html', form = form, pb = pb)
  else:
    if form.visible.data == 'True':
      vis = True
    else:
      vis = False
    Problem.query.filter_by(id = problemid).update({'title': form.title.data, 'description': form.description.data, 
      'pbinput': form.pbinput.data, 'pboutput': form.pboutput.data, 
      'sinput': form.sinput.data, 'soutput': form.soutput.data, 'hint': form.hint.data, 
      'timelmt' : form.timelmt.data, 'memorylmt' : form.memorylmt.data, 'visible':vis })
    db.session.commit()
    db.session.close()
    return redirect(url_for('Showprb', problemid = problemid))

@app.route('/delprb/')
@app.route('/delprb/<problemid>')
def Deleteprb(pbid):
  pb = Problem.query.get(pbid).delete()
  db.session.commit()
  db.session.close()
  return redirect( url_for('Problems') )

@app.route('/setvisibility/<int:pbid><visibility>')
def Set_visibility(pbid, visibility):
  if visibility == 'False':
    vis  = False
  else:
    vis = True
  print vis
  Problem.query.filter_by(id=pbid).update({'visible': vis})
  db.session.commit()
  # db.session.close()
  return redirect(url_for('Problems'))
