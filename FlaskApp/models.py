from datetime import datetime
from FlaskApp import db,app , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(ins_id):
	return Institute.query.get(int(ins_id))


class Institute(db.Model , UserMixin):
	id = db.Column(db.Integer , primary_key = True)
	ins_name = db.Column(db.String(70),unique = True,nullable = False)
	admin_name = db.Column(db.String(50),nullable = False)
	address = db.Column(db.String(100),nullable=False)
	mobile_no = db.Column(db.Integer,unique = True,nullable=False)
	no_of_students = db.Column(db.Integer,nullable=False)
	no_of_staff = db.Column(db.Integer,nullable=False)
	email = db.Column(db.String(120),unique = True,nullable = False)
	password = db.Column(db.String(60),nullable=False)
	scope = db.Column(db.String(200),nullable=False)
	ins_img = db.Column(db.String(20), default='default.jpg')
	posts = db.relationship('Event',backref='host',lazy=True)

	def __repr__(self):
		return f"Institute('{self.ins_name}')"


class Event(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	title = db.Column(db.String(70),nullable = False)
	short_disc = db.Column(db.String(150),nullable = False)
	long_disc = db.Column(db.String(2000),nullable=False)
	poster = db.Column(db.String(20), default='default.jpg')
	reg_last_date = db.Column(db.DateTime , nullable=False)
	event_date = db.Column(db.DateTime , nullable=False)
	ins_id = db.Column(db.Integer,db.ForeignKey('institute.id'),nullable=False)

	def __repr__(self):
		return f"Event ('{self.title}','{self.short_disc}')"		