from . import db
from flask_login import UserMixin
import enum


class Role(enum.Enum):
   student = "student"
   admin = "admin"
   teacher = "teacher"


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(150), unique=True, nullable=False) 
   password = db.Column(db.String(150), nullable=False) 
   role = db.Column(db.String(50), nullable=False) 
   enrol = db.relationship('Enrol')




class StudentInfo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   last_name = db.Column(db.String(120), nullable=False)
   middle_name = db.Column(db.String(120))
   first_name = db.Column(db.String(120), nullable=False)
   suffix = db.Column(db.String(120), nullable=False)
   date_of_birth = db.Column(db.String, nullable=False)
   gender = db.Column(db.String(10), nullable=False)
   nationality = db.Column(db.String(100), nullable=False)
   address = db.Column(db.String(255), nullable=False)
   parent_guardian_name = db.Column(db.String(150), nullable=False)
   email_gp = db.Column(db.String(150), nullable=False)
   relationship_to_student = db.Column(db.String(100), nullable=False)
   contact_number = db.Column(db.String(20), nullable=False)
   emergency_contact_name = db.Column(db.String(150), nullable=False)
   emergency_relationship = db.Column(db.String(100), nullable=False)
   emergency_contact_number = db.Column(db.String(20), nullable=False)
   user = db.relationship('User')




class AnnouncementAdmin(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(150), nullable=False)
   description = db.Column(db.Text, nullable=False)
   created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class AnnouncementTeacher(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(150), nullable=False)
   description = db.Column(db.Text, nullable=False)
   created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




class Schedule(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), nullable=False, unique=True)


class Level(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), nullable=False, unique=True)


class Subject(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), nullable = False, unique=True)


class Section(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
   schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
   subject_id = db.Column(db.Integer, db.ForeignKey ('subject.id'), nullable=False)
   time_from = db.Column(db.String(5), nullable=False)  # Format: HH:MM
   time_to = db.Column(db.String(5), nullable=False)    # Format: HH:MM
   instructor = db.Column(db.String(100), nullable=False)



class Enrol(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
   status = db.Column(db.String(50), default = "Pending")