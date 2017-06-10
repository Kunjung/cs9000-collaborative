from app import db
from app.models import *
import pandas as pd

df = pd.read_csv('movies.csv', sep=',')

db.drop_all()
db.create_all()

for d in df.values:
	try:
		id, title = d[0], d[1]
		movie = Movie(id, title)
		db.session.add(movie)
	except:
		print('failed in {}'.format(d[0]))
	

db.session.commit()
print("Done loading data")