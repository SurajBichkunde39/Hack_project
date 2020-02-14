from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import StringField , PasswordField , SubmitField , BooleanField , TextAreaField , IntegerField , DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
import phonenumbers


class RegistrationForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired() , Email()])
	password = PasswordField('Password' , validators=[DataRequired()])
	confirm_password =  PasswordField('Conform Password', validators=[DataRequired() , EqualTo('password')])
	submit = SubmitField('Varify Email')

class InfoForm(FlaskForm):
	ins_name = StringField('Institute Name',validators=[DataRequired(),Length(min=2,max=50)])
	admin_name = StringField('Admin Name',validators=[DataRequired()])
	address = StringField('Address',validators=[DataRequired()])
	mobile_no = StringField('Mobile no.', validators=[DataRequired()])
	no_of_students = IntegerField('No of Students' , validators=[DataRequired()])
	no_of_staff = IntegerField('No of Staff Members' , validators=[DataRequired()])
	scope = StringField('Overall Scope of Students')
	ins_img = FileField('Picture of Institute' , validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Save Profile')

	def validate_phone(self, mobile_no):
		try:
			p = phonenumbers.parse(mobile_no.data)
			if not phonenumbers.is_valid_number(p):
				raise ValueError()
		except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
				raise ValidationError('Invalid mobile_no number')

class CreatePostForm(FlaskForm):
	title = StringField('Title',validators = [DataRequired() ,Length(min=2,max=30)])
	short_disc = StringField('Short Discription',validators = [DataRequired() ,Length(min=2,max=100)])
	long_disc = TextAreaField('Long Discription',)
	poster = FileField('Event Poster' , validators=[FileAllowed(['jpg','png'])])
	reg_last_date = DateField('Last Date For Registration',validators=[DataRequired()])
	event_date = DateField('Event Date',validators=[DataRequired()])
	submit = SubmitField('Post Event')


class InvitationForm(FlaskForm):
	pass


class RespondForm(FlaskForm):
	pass



class LoginForm(FlaskForm):
	email = StringField('Email',
		validators = [DataRequired() , Email()])
	password = PasswordField('Password' , validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
	email = StringField('Email',
		validators = [DataRequired() , Email()])
	submit = SubmitField('Request Password Reset ')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password' , validators=[DataRequired()])
	confirm_password =  PasswordField('Conform Password',
		validators=[DataRequired() , EqualTo('password')])
	submit = SubmitField('Reset Password')
