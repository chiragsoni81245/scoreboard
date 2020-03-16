from collections import defaultdict
import sqlite3 as sq3

db = sq3.connect("score.db")
c = db.cursor()


handle_with_level= {"ziddi":4,"tanu38":4,"chiragsoni812":4,"mohi07":3,"chauhan002":3,\
"shivambhat":3,"sp_":2,"Nishant_Rao":2,"Aka_coder":2,"hr4_harsh":2,"AM_coder":1,\
"ankitkochar1578":1,'_viru_':4,'hitzmac':1,'khiladi.07':1,'_chanchal':2,"shubhamz950":4}

data = defaultdict(dict)
data = { i:{"star":handle_with_level[i],"points":0,"pointer":"0","accepted":0,"wrong":0} for i in handle_with_level }

spointers = {'ziddi': 73315082, 
				'tanu38': 73127093, 
				'chiragsoni812': 72939979, 
				'mohi07': 73199151, 
				'chauhan002': 73326905,
				 'shivambhat': 73358069, 
				 'sp_': 73334404, 
				 'Nishant_Rao': 73311376,
				  'Aka_coder': 73336145, 
				  'hr4_harsh': 73344255, 
				  'AM_coder': 73355874, 
				  'ankitkochar1578': 73330313, 
				  '_viru_': 71858618, 'hitzmac': 73313399, 'khiladi.07': 73357095, '_chanchal': 73342154, 'shubhamz950': 55379990}

print(data)

for i in data:
	data[i]['pointer']=spointers[i]



q='''create table score( star integer,
						name VARCHAR,
						points integer,
						pointer VARCHAR,
						accepted integer,
						wrong integer ); '''


q2='''create table aw( name VARCHAR,
						aw integer,
						rating integer,
						point integer ); '''


c.execute( q2 )
c.execute( q )

for i in data:
	print(i)
	q1='''insert into score(star,name,points,pointer,accepted,wrong) values({},'{}',{},{},{},{})'''.format(data[i]['star'],
																					i,
																					data[i]['points'],
																					data[i]['pointer'],0,0)
	print(q)


	c.execute( q1 )

db.commit()
db.close()