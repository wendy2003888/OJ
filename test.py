from flask import Flask, url_for, render_template, request
from forms import RegisterForm
from fileconfig import Registererr


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
	if(request.method == 'GET' ):
		return render_template("sign_up.html", form = form)
	else:
		if form.validate():
			error = None
		else:
			error = Registererr
	if error == None :
		return render_template('homepage.html')
	else:
		return render_template('sign_up.html', form = form, error = error)


if __name__ == '__main__':
	app.run(debug = True)