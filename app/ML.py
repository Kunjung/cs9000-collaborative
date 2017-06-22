# Mid-course Happiness Score: 23
from .models import *

THRESHOLD = 0.5
NUMBER_OF_MOVIES_TO_RECOMMEND = 10
THRESHOLD_TO_BEGIN_ALGORITHM = 7


def get_rating_for_ancient_user(user_id, movie_id):
	query = ancient_ratings.select('rating').where(ancient_ratings.c.user_id==user_id).where(ancient_ratings.c.movie_id==movie_id)
	values = db.session.execute(query).first()
	rating = values[2]
	return rating

def get_rating(user_id, movie_id):
	query = ratings.select('rating').where(ratings.c.user_id==user_id).where(ratings.c.movie_id==movie_id)
	values = db.session.execute(query).first()
	rating = values[2]
	return rating

def get_all_users():
	return AncientUser.query.all()

def get_all_movies():
	return Movie.query.all()

# Returns a distance-based similarity score for person1 and person2
def similarity_distance(user1, user2):
	# Get the list of shared_movies
	si={}

	user1_movies = user1.rated
	user2_movies = user2.rated

	sum_of_squares = 0
	for movie in user1_movies:
		if movie in user2_movies:
			si[movie.id]=1

	# if they have no ratings in common, return 0
	if len(si) == 0: return 0

	for movie in user1_movies:
		if movie in user2_movies:
			#Get the ratings for the particular movie
			user1_rating = get_rating(user1.id, movie.id)
			user2_rating = get_rating_for_ancient_user(user2.id, movie.id)

			if user1_rating is None or user2_rating is None:
				continue

			# Add up the squares of all the differences
			diff = user1_rating - user2_rating
			sum_of_squares = sum_of_squares + diff * diff
					
	
	return 1/(1+sum_of_squares)



# Gets recommendations for a person by using a weighted average
# of every other user's rankings

def predict_movies_for_user(user, users):
	totals={}
	simSums={}

	### At the very beginning when the user hasn't rated anything
	if len([movie.id for movie in user.rated]) <= THRESHOLD_TO_BEGIN_ALGORITHM:
		return Movie.query.limit(THRESHOLD_TO_BEGIN_ALGORITHM + 1)

	for other in users:
		# Speed Up by limiting number of movies
		# if len(totals) >= NUMBER_OF_MOVIES_TO_RECOMMEND:
		# 	break

		# don't compare me to myself
		if other.id == user.id: continue

		sim = similarity_distance(user, other)

		# ignore scores less than the threshold
		if sim <= THRESHOLD:
			continue


		for movie in other.rated:
			# only score movies I haven't seen yet
			if movie not in user.rated:

				rating = get_rating_for_ancient_user(other.id, movie.id)
				if rating is None:
					continue
				# Similarity * Score

				totals.setdefault(movie.id ,0)
				totals[movie.id] += rating * sim

				# Sum of similarities
				simSums.setdefault(movie.id ,0)
				simSums[movie.id] += sim

			
	# Create the normalized list
	rankings=[(total/simSums[movie.id], movie_id) for movie_id, total in totals.items()]

	# Return the sorted list
	rankings.sort()
	rankings.reverse()
	movies = [Movie.query.get(id) for ranking, id in rankings]
	return movies



