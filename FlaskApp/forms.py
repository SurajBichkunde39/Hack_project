from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import StringField , PasswordField , SubmitField , BooleanField , TextAreaField , IntegerField , DateField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
import phonenumbers


class RegistrationForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired() , Email()])
	password = PasswordField('Password' , validators=[DataRequired()])
	conform_password =  PasswordField('Conform Password', validators=[DataRequired() , EqualTo('password')])
	submit = SubmitField('Varify Email')

class InfoForm(FlaskForm):
	ins_name = StringField('Instute Name',validators=[DataRequired(),Length(min=2,max=50)])
	admin_name = StringField('Admin Name',validators=[DataRequired()])
	phone = StringField('Phone', validators=[DataRequired()])
	no_of_students = IntegerField('No of Students' , validators=[DataRequired()])
	no_of_staff = IntegerField('No of Staff Members' , validators=[DataRequired()])
	scope = StringField('Overall Scope of Students')
	ims_img = FileField('Picture of Instute' , validators=[DataRequired() , FileAllowed(['jpg','png'])])

	def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class CreatePostForm(FlaskForm):
	title = StringField('Title',validators = [DataRequired() ,Length(min=2,max=30)])
	short_disc = StringField('Short Discription',validators = [DataRequired() ,Length(min=2,max=100)])
	long_disc = TextAreaField('Long Discription',)
	poster = FileField('Event Poster' , validators=[DataRequired() , FileAllowed(['jpg','png'])])
	reg_last_date = DateField('Last Date For Registration',validators=[DataRequired()])
	event_date = DateField('Event Date',validators=[DataRequired()])


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
	conform_password =  PasswordField('Conform Password',
		validators=[DataRequired() , EqualTo('password')])
	submit = SubmitField('Reset Password')
