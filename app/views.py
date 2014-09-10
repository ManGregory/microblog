from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname' : 'Greg'}
	posts = [
		{
			'author' : {'nickname': 'John'},
			'body' : 'Beautiful day in Portland!',
			'date' : '24.03.2014' 
		},
		{
			'author' : {'nickname': 'Susan'},
			'body' : 'The Avengers movie was cool!',
			'date' : '05.08.2014' 
		}
	]
	return render_template("index.html", 
		title = 'Home',
		user = user,
		posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html',
		title = 'Sign in',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])	