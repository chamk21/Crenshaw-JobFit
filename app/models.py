from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    admin = db.Column(db.Boolean)
    assessor = db.Column(db.Boolean)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    image_file=db.Column(db.String(20),nullable=True,default='default.jpg')
    solution_answered_by=db.relationship('Solution', backref='User', lazy='dynamic')
    feedback_for=db.relationship('Feedback', backref='User', lazy='dynamic')
    verb_answered_by=db.relationship('VerbReasonAnswer', backref='User', lazy='dynamic')
    apt_answered_by=db.relationship('AptAnswer', backref='User', lazy='dynamic')
    Tasks_for=db.relationship('Tasks', backref='User', lazy='dynamic')


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.Text,nullable=False)
    set_about=db.Column(db.Text,nullable=True)
    setaddedtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    question_id=db.relationship('quiz', backref='Set', lazy='dynamic')
    task_set=db.relationship('Tasks', backref='Set', lazy='dynamic')

class quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.Text,nullable=False)
    setid=db.Column(db.Integer, db.ForeignKey('set.id'))
    setname=db.Column(db.Text,nullable=False)
    time_limit=db.Column(db.Integer, nullable=True)
    quizaddedtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    solution_id=db.relationship('Solution', backref='quiz', lazy='dynamic')
    
    def __repr__(self):
        return '<timelimit {}>'.format(self.time_limit) 
           
class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Solution = db.Column(db.Text,nullable=False)
    problem_id=db.Column(db.Integer, db.ForeignKey('quiz.id'))
    problemname=db.Column(db.Text,nullable=False)
    setname=db.Column(db.Text,nullable=True)
    solutionaddedtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    problem_answered_by=db.Column(db.Integer, db.ForeignKey('user.id'))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    setname = db.Column(db.String(140))
    aptitudefeedback = db.Column(db.String(140))
    content= db.Column(db.Text, nullable=False)
    feedback_for=db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140),nullable=True)
    task_posted_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    side_notes= db.Column(db.Text, nullable=False)
    task_completed_by_date=db.Column(db.Text, nullable=True)
    task_for=db.Column(db.Integer, db.ForeignKey('user.id'))
    task_set=db.Column(db.Integer, db.ForeignKey('set.id'))

class Aptitude(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(140),nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    option_one= db.Column(db.String(140), nullable=True)
    option_two= db.Column(db.String(140), nullable=True)
    option_three= db.Column(db.String(140), nullable=True)
    option_four= db.Column(db.String(140), nullable=True)
    option_five= db.Column(db.String(140), nullable=True)

class AptAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apt_answered_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    apt_question=db.Column(db.String(140), nullable=False)
    apt_choice=db.Column(db.String(140), nullable=False)
    
class VerbReason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(140),nullable=True)
    time_limit=db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    option_one= db.Column(db.String(140), nullable=True)
    option_two= db.Column(db.String(140), nullable=True)
    option_three= db.Column(db.String(140), nullable=True)
    
class VerbReasonAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verb_answered_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    verb_question=db.Column(db.String(140), nullable=False)
    verb_choice=db.Column(db.String(140), nullable=False)
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))