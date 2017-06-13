# Mid-course Happiness Score: 23
from .models import *
from math import sqrt


def get_rating(user_id, movie_id):
	query = ancient_ratings.select('rating').where(ancient_ratings.c.user_id==user_id).where(ancient_ratings.c.movie_id==movie_id)
	values = db.session.execute(query).first()
	rating = values[2]
	return rating

def get_all_users():
	return AncientUser.query.all()

def get_all_movies():
	return Movie.query.all()

def get_movies(user_id):
	query = ancient_ratings.select('movie_id').where(ancient_ratings.c.user_id==user_id)
	values = db.session.execute(query).all()
	user_movies = values[1]
	return user_movies

# Returns a distance-based similarity score for person1 and person2
def sim_distance(user1, user2):
	# Get the list of shared_movies
	si={}

	user1_movies = user1.rated
	user2_movies = user2.rated

	for movie in user1_movies:
		if movie in user2_movies:
			si[movie.id]=1

		# if they have no ratings in common, return 0
		if len(si)==0: return 0

		#Get the ratings for the particular movie
		user1_ratings = get_rating(user1.id, movie.id)
		user2_ratings = get_rating(user2.id, movie.id)

		# Add up the squares of all the differences
		sum_of_squares=sum([pow(user1_ratings - user2_ratings, 2)
					for movie1 in user1_movies if movie1 in user2_movies])

return 1/(1+sum_of_squares)



# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def predict_movies_for_user(user, users, n=20):
	totals={}
	simSums={}

	for other in users:
		# don't compare me to myself
		if other.id == user.id: continue
		sim = similarity_distance(user, other)

		# ignore scores of zero or lower
		if sim <=0: continue
		for movie in other.rated:

			# only score movies I haven't seen yet
			if movie not in user.rated ==0:

				# Similarity * Score
				totals.setdefault(movie.id ,0)
				totals[movie.id] += get_rating(other.id, movie.id) * sim

				# Sum of similarities
				simSums.setdefault(movie.id ,0)
				simSums[movie.id] += sim

		# Create the normalized list
	rankings=[(total/simSums[movie.id], movie_id) for movie_id, total in totals.items()]

# Return the sorted list
rankings.sort()
rankings.reverse()
return rankings[:n]




