from flask import Flask, url_for, render_template, request
from forms import RegisterForm
from config import Useriderr, Passworderr

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def Homepage():
	return render_template('homepage.html')

@app.route('/login')
def Login():
	return render_template('login.html')

@app.route("/sign_up", methods = ['GET', 'POST'])
def Sign_up():
	form = RegisterForm()
	if(request.method == 'POST' ):
		if not form.validate_userid():
			error = Useriderr
		elif not form.valiate_password():
			error = Passworderr
		else:
			error = None
		if error == None :
			return render_template('homepage.html')
		else:
			return render_template('sign_up.html', form = form, error = error)
	return render_template("sign_up.html", form = form)


if __name__ == '__main__':
	app.run()

