from flask import render_template , url_for , flash , redirect , request , abort, session
from PIL import Image
from FlaskApp import app, db, bcrypt 
from FlaskApp.forms import LoginForm , RegistrationForm , RequestResetForm , ResetPasswordForm , InfoForm , CreatePostForm , ResponseForm
from FlaskApp.models import Institute, Event
from flask_login import login_user , current_user , logout_user , login_required

@app.route('/')
@app.route('/home')
def home():
	events = Event.query.order_by(Event.reg_last_date.desc())
	return render_template('home.html',events=events)


@app.route('/about')
def about():
	return render_template('about.html',title='About')


@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		ins = Institute.query.filter_by(email=form.email.data).first()
		if ins and bcrypt.check_password_hash(ins.password,form.password.data):
			login_user(ins,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
			flash(f'You have successfully Logged in','success')
			return redirect(url_for('home'))
		else:
			flash(f'wrong mail id or password','danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		session['email_id']=form.email.data
		session['hashed_password']=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		flash('Your account has been created! Please complete your profile.','success')
		return redirect(url_for('info'))
	return render_template('register.html' ,title='Register', form = form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/ins_profiles',picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/info',methods=['GET','POST'])
def info():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = InfoForm()
	if form.validate_on_submit():
		if form.ins_img.data:
			picture_file = save_picture(form.ins_img.data)
			institute = Institute(ins_name=form.ins_name.data, password=session['hashed_password'],email=session['email_id'], admin_name=form.admin_name.data,
					address=form.address.data,mobile_no=form.mobile_no.data,ins_img=picture_file,no_of_students=form.no_of_students.data,
					no_of_staff=form.no_of_staff.data,scope=form.scope.data)

		else:
			institute = Institute(ins_name=form.ins_name.data, password=session['hashed_password'],email=session['email_id'], admin_name=form.admin_name.data,
					address=form.address.data,mobile_no=form.mobile_no.data,no_of_students=form.no_of_students.data,
					no_of_staff=form.no_of_staff.data,scope=form.scope.data)
		db.session.add(institute)
		db.session.commit()
		flash('Information updated, you can now login.','success')
		return redirect(url_for('login'))
	
	return render_template('info.html', title='Info', form = form)


@app.route('/request_reset',methods=['GET','POST'])
def request_reset():
	form = RequestResetForm()
	if form.validate_on_submit():
		flash(f'An Email has been sent to your account with further instructions.','success')
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
		eve1 = Event(title=form.title.data,short_disc=form.short_disc.data,long_disc=form.long_disc.data,poster = form.poster.data,reg_last_date=form.reg_last_date.data,event_date=form.event_date.data,ins_id=current_user.id)
		db.session.add(eve1)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create_post.html', title='Create Event', form=form)

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
	return render_template('account.html', title='Account')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/event/<int:event_id>")
def event(event_id):
		event = Event.query.get_or_404(event_id)
		return render_template('event.html',title=event.title , event = event)

@app.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.host != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!','success')
    return redirect(url_for('home'))

@app.route("/institute_info/<int:ins_id>")
def institute_info(ins_id):
	institute = Institute.query.get_or_404(ins_id)
	events = Event.query.filter_by(host=institute).order_by(Event.event_date.desc())
	return render_template('institute_info.html',title=institute.ins_name,institute=institute , events = events)


@app.route("/response" , methods=['GET','POST'])
def response():
	form = ResponseForm()
	if form.validate_on_submit() and 'submit' in request.form:
		flash('Your Response has benn sent to the event host institute')
		return redirect(url_for('home'))
	elif form.validate_on_submit() and 'add' in request.form:
		return redirect(url_for('response'))
	return render_template('response.html',title="Send Response",form=form)