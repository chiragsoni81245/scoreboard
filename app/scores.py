

from collections import defaultdict
import sqlite3 as sq3

db = sq3.connect("score.db")
c = db.cursor()


handle_with_level= {"ziddi":4,"tanu38":4,"chiragsoni812":4,"mohi07":3,"chauhan002":3,\
"shivambhat":3,"sp_":2,"Nishant_Rao":2,"Aka_coder":2,"hr4_harsh":2,"AM_coder":1,\
"ankitkochar1578":1,'_viru_':4,'hitzmac':1,'khiladi.07':1,'_chanchal':2,"shubhamz950":1}

data = defaultdict(dict)
data = {i:{"star":handle_with_level[i],"points":0,"pointer":"0"} for i in handle_with_level}

q='''create table score( star integer,
						name VARCHAR,
						points integer,
						pointer VARCHAR ); '''



c.execute( q )

for i in data:
	print(i)
	q1='''insert into score(star,name,points,pointer) values({},'{}',{},{})'''.format(data[i]['star'],
																					i,
																					data[i]['points'],
																					data[i]['pointer'])
	c.execute( q1 )

db.commit()
db.close()