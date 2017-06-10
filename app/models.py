from app import db
from flask_login import UserMixin

ratings = db.Table('ratings',
		db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
		db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
		db.Column('rating', db.Integer)
	)

ancient_ratings = db.Table('ancient_ratings',
		db.Column('user_id', db.Integer, db.ForeignKey('ancient_users.id')),
		db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
		db.Column('rating', db.Float)
	)

class AncientUser(db.Model):
	__tablename__ = 'ancient_users'
	id = db.Column(db.Integer, primary_key=True)
	rated = db.relationship('Movie', secondary=ancient_ratings, backref='ancient_raters', lazy='dynamic')

	def __init__(self, id):
		self.id = id

	def __repr__(self):
		return '<Ancient User %r>' % self.id


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(42), unique=True)
	password = db.Column(db.String(42))
	rated = db.relationship('Movie', secondary=ratings, backref='raters', lazy='dynamic')
	

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def __repr__(self):
		return '<User %r>' % self.username

class Movie(db.Model):
	__tablename__ = 'movies'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	
	def __init__(self, id, title):
		self.id = id
		self.title = title

	def __repr__(self):
		return '<Movie %r>' % self.title

# use this to update or get data from ratings table
######################
# query = ratings.update().where(
#     ratings.c.user_id == user1.id
# ).where(
#     ratings.c.movie_id == movie1.id
# ).values(rating=new_rating)
#
# db.session.execute(query)
# val = db.session.execute(query).first()[2]