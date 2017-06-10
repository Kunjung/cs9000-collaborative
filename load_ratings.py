from app import db
from app.models import *
import pandas as pd
	
df = pd.read_csv('ratings.csv', sep=',')

for d in df.values:
	user_id, movie_id, rating = d[0], d[1], d[2]
	query = ancient_ratings.insert().values(user_id=user_id, movie_id=movie_id, rating=rating)
	db.session.execute(query)
	

db.session.commit()
print("Done loading data")