from flask import render_template
from app import app

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