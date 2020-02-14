from flask import render_template , url_for , flash , redirect , request , abort
from FlaskApp import app 
from FlaskApp.forms import LoginForm , RegistrationForm , RequestResetForm , ResetPasswordForm , InfoForm , CreatePostForm

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		return redirect(url_for('register'))
	return render_template('login.html',form = form)

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		return redirect(url_for('info'))
	return render_template('register.html' , form = form)

@app.route('/info',methods=['GET','POST'])
def info():
	form = InfoForm()
	if form.validate_on_submit():
		return redirect(url_for('info'))
	return render_template('info.html',form = form)


@app.route('/request_reset',methods=['GET'])
def request_reset():
	form = RequestResetForm()
	if form.validate_on_submit():
		return redirect(url_for('reset_password'))
	return render_template('request_reset.html',form = form)

@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
	form = ResetPasswordForm()
	if form.validate_on_submit():
		return redirect(url_for('home'))
	return render_template('reset_password.html',form = form)

@app.route('/create_post',methods=['GET','POST'])
def create_post():
	form = CreatePostForm()
	if form.validate_on_submit():
		return redirect(url_for('home'))
	return render_template('create_post.html',form=form)

