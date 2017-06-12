# Mid-course Happiness Score: 23
from .models import *

def get_rating(user_id, movie_id):
	query = ancient_ratings.select('rating').where(ancient_ratings.c.user_id==user_id).where(ancient_ratings.c.movie_id==movie_id)
	values = db.session.execute(query).first()
	rating = values[2]
	return rating

def get_all_users():
	return AncientUser.query.all()

def get_all_movies():
	return Movie.query.all()

def predict_movies_for_user(userA, users, movies):
	### TO DO
	### returns a list of movies arranged in descending order based on minimum distance
	return Movie.query.limit(50)