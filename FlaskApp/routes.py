from flask import render_template , url_for , flash , redirect , request , abort
from FlaskApp import app, db, bcrypt 
from FlaskApp.forms import LoginForm , RegistrationForm , RequestResetForm , ResetPasswordForm , InfoForm , CreatePostForm
from FlaskApp.models import Institute, Event
from flask_login import login_user,current_user,logout_user,login_required

@app.route('/')
@app.route('/home')
def home():
	events = Event.query.all()
	return render_template('home.html',events=events)


@app.route('/about')
def about():
	return render_template('about.html',title='About')


@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		return redirect(url_for('register'))
	return render_template('login.html',title='Login', form = form)

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		institute = Institute(email=form.email.data, password=hashed_password)
		db.session.add(institute)
		flash('Your account has been created! Please complete your profile.','success')
		return redirect(url_for('info'))
	return render_template('register.html' ,title='Register', form = form)

@app.route('/info',methods=['GET','POST'])
def info():
	form = InfoForm()
	if form.validate_on_submit():
		institute = Institute(ins_name=form.ins_name.data,admin_name=form.admin_name.data,address=form.address.data,mobile_no=form.mobile_no.data,no_of_students=form.no_of_students.data,no_of_staff=form.no_of_staff.data,scope=form.scope.data,ins_img=form.ins_img.data)
		db.session.add(institute)
		db.session.commit()
		flash('Information updated, you can now login.','success')
		return redirect(url_for('login'))
	return render_template('info.html', title='Info', form = form)


@app.route('/request_reset',methods=['GET'])
def request_reset():
	form = RequestResetForm()
	if form.validate_on_submit():
		return redirect(url_for('reset_password'))
	return render_template('request_reset.html', title='Reset Password', form = form)

@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
	form = ResetPasswordForm()
	if form.validate_on_submit():
		return redirect(url_for('home'))
	return render_template('reset_password.html', title='Reset Password', form = form)

@app.route('/create_post',methods=['GET','POST'])
def create_post():
	form = CreatePostForm()
	if form.validate_on_submit():
		return redirect(url_for('home'))
	return render_template('create_post.html', title='Create Event', form=form)

@app.route('/account',methods=['GET','POST'])
def account():
	return render_template('account.html', title='Account')

@app.route('/logout')
def logout():
	return redirect(url_for('home'))


@app.route("/event/<int:event_id>")
def event(event_id):
		event = Event.query.get_or_404(event_id)
		return render_template('event.html',title=event.title , event = event)

@app.route("/institute_info/<int:ins_id>")
def institute_info(ins_id):
	institute = Institute.query.get_or_404(ins_id)
	events = Event.query.filter_by(host=institute).order_by(Event.event_date.desc())
	return render_template('institute_info.html',title=institute.ins_name,institute=institute , events = events)
