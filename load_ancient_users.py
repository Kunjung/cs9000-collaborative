from app import db
from app.models import *
import pandas as pd
	
df = pd.read_csv('ratings.csv', sep=',')

users = [d[0] for d in df.values]
users = set(users)
for	user_id in users:
	ancient_user = AncientUser(user_id)
	db.session.add(ancient_user)
	
db.session.commit()
print("Done loading data")