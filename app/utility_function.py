import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from threading import Thread
import sqlite3 as sq3
import time

# AW = Accepted Wrong

def q_generator( handle,aw,rating,point,query_list,question,date_time ):
	q = "insert into aw(name,aw,rating,point,question_txt,question_link,date_time) values('{}',{},{},{},'{}','{}','{}');".format(handle,
																											aw,
																											rating,
																											point,
																											question.text.strip().strip("\n").replace("'",""),
																											question['href'].strip(),
																											date_time )
	
	query_list.append( q )


def func_points(handle,rating,data,AW,query_list,question,date_time):

	if AW:
		aw=1
	else:
		aw=0

	if data[handle]["star"] == 4:
		if rating < 1100:
			if AW==True:
				data[handle]["points"] += 30
				q_generator( handle,aw,rating,30,query_list,question,date_time )
			else:
				data[handle]["points"] -= 6	
				q_generator( handle,aw,rating,-6,query_list,question,date_time )

		elif rating > 1400:
			if AW==True:
				data[handle]["points"] += 100
				q_generator( handle,aw,rating,100,query_list,question,date_time )

			else:
				data[handle]["points"] -= 20
				q_generator( handle,aw,rating,-20,query_list,question,date_time )

		else:
			if AW==True:
				data[handle]["points"] += ((rating-1100)/100)*10+50
				q_generator( handle,aw,rating, ((rating-1100)/100)*10+50,query_list,question,date_time )

			else:
				data[handle]["points"] -= (((rating-1100)/100)*10+50)//5
				q_generator( handle,aw,rating, -(((rating-1100)/100)*10+50)//5,query_list,question,date_time )


	if data[handle]["star"] == 3:
		if rating < 1000:
			if AW==True:
				data[handle]["points"] += 30
				q_generator( handle,aw,rating,30,query_list,question,date_time )

			else:
				data[handle]["points"] -= 6
				q_generator( handle,aw,rating,-6,query_list,question,date_time )

		elif rating > 1200:
			if AW==True:
				data[handle]["points"] += 100
				q_generator( handle,aw,rating,100,query_list,question,date_time )

			else:
				data[handle]["points"] -= 20
				q_generator( handle,aw,rating,-20,query_list,question,date_time )

		else:
			if AW==True:
				data[handle]["points"] += ((rating-1000)/100)*25+50
				q_generator( handle,aw,rating,((rating-1000)/100)*25+50,query_list,question,date_time )

			else:
				data[handle]["points"] -= (((rating-1000)/100)*25+50)//5
				q_generator( handle,aw,rating,-(((rating-1000)/100)*25+50)//5,query_list,question,date_time )


	if data[handle]["star"] == 2:
		if rating < 900:
			if AW==True:
				data[handle]["points"] += 30
				q_generator( handle,aw,rating,30,query_list,question,date_time )

			else:
				data[handle]["points"] -= 6
				q_generator( handle,aw,rating,-6,query_list,question,date_time )

		elif rating > 1100:
			if AW==True:
				data[handle]["points"] += 100
				q_generator( handle,aw,rating,100,query_list,question,date_time )

			else:
				data[handle]["points"] -= 20
				q_generator( handle,aw,rating,-20,query_list,question,date_time )


		else:
			if AW==True:
				data[handle]["points"] += ((rating-900)/100)*25+50
				q_generator( handle,aw,rating,((rating-900)/100)*25+50,query_list,question,date_time )

			else:
				data[handle]["points"] -= (((rating-900)/100)*25+50)//5
				q_generator( handle,aw,rating,-(((rating-900)/100)*25+50)//5,query_list,question,date_time )


	if data[handle]["star"] == 1:
		if rating < 700:
			if AW==True:
				data[handle]["points"] += 30
				q_generator( handle,aw,rating,30,query_list,question,date_time )

			else:
				data[handle]["points"] -= 6
				q_generator( handle,aw,rating,-6,query_list,question,date_time )

		elif rating > 900:
			if AW==True:
				data[handle]["points"] += 100
				q_generator( handle,aw,rating,100,query_list,question,date_time )

			else:
				data[handle]["points"] -= 20
				q_generator( handle,aw,rating,-20,query_list,question,date_time )

		else:
			if AW==True:
				data[handle]["points"] += ((rating-700)/100)*25+50
				q_generator( handle,aw,rating,((rating-700)/100)*25+50,query_list,question,date_time )

			else:
				data[handle]["points"] -= (((rating-700)/100)*25+50)//5
				q_generator( handle,aw,rating,-(((rating-700)/100)*25+50)//5,query_list,question,date_time )


	return data[handle]["points"]	


def fetch_rating(link):

	r = requests.get(link)
	soup = BeautifulSoup(r.text,"html.parser")
	try:
		rating = int(soup.find("span",{"class":"tag-box","title":"Difficulty"}).text.strip().strip("*"))
	except:
		rating = -1
	return rating

def get_questions( handle, page,data ):
	link = "https://codeforces.com/submissions/{}/page/{}".format(handle,page)
	r = requests.get(link)
	soup = BeautifulSoup(r.text,"html.parser")
	table = soup.find_all("table",{"class":["status-frame-datatable"]})[0]
	trs = table.find_all("tr")[1:]

	c = 0
	w = 0
	submission = []
	br=0
	for i in trs:
		point = i.find_all("td")[0].text.strip()
		question = i.find_all("td")[3].find("a")
		date_time = i.find_all("td")[1].text.strip().strip("\n")

		if str(point) == str(data[handle]["pointer"]):
			br=1
			break

		# print( i )
		# print( i.find_all("td")[5].find_all("span") )
		try: 
			if i.find_all("td")[5].text.find("Running")==-1 and i.find_all("td")[5].text.find("queue")==-1:
				verdict = i.find_all("td")[5].find_all("span")[1].text
				if verdict == "Accepted":
					c = c + 1
					link = "https://codeforces.com"+i.find_all("td")[3].a['href']
					rating = fetch_rating(link)
					if rating!=-1:
						submission.append( (rating,question,True,date_time) )
				else:
					w = w + 1
					link = "https://codeforces.com"+i.find_all("td")[3].a['href']
					rating = fetch_rating(link)
					if rating!=-1:
						submission.append( (rating,question,False,date_time) )
			else:
				br=2
				break
		except:
			pass
		
	return  [ [c,w,submission], br ]


def start_pointer( handle ):
	link = "https://codeforces.com/submissions/{}/page/1".format(handle)
	r = requests.get(link)
	soup = BeautifulSoup(r.text,"html.parser")
	table = soup.find_all("table",{"class":["status-frame-datatable"]})[0]
	trs = table.find_all("tr")[1:]
	fp = trs[0].find_all("td")[0].text.strip().strip("\n")
	return fp

def page_traversal(handle,data,query_list):
	page=1
	c,w,submission=0,0,[]
	fp = start_pointer( handle )
	time.sleep( 2 )
	while(1):
		result = get_questions( handle,page,data )
		l=result[0]
		c+=l[0]
		w+=l[1]
		submission+=l[2]

		if result[1]==2:
			break
			
		if result[1]==1:
			data[handle]["pointer"] = fp
			break

		page+=1

	for i in submission:
		func_points(handle,i[0],data,i[2],query_list,i[1],i[3])

	data[handle]['accepted'] += c
	data[handle]['wrong'] += w

	print( "{} Accepted:{}, Wrong:{}, Points:{}\n".format( handle, c,w, data[handle]['points'] ) )

def update_point( handle,data,query_list ):
	page_traversal(handle,data,query_list)

def score_count( handles ):
	db = sq3.connect("score.db")
	c = db.cursor()
	q="select star,name,points,pointer,accepted,wrong from score;"
	c.execute(q)
	d = c.fetchall()
	data = defaultdict(dict)
	data = { i[1]:{'star':i[0],'points':i[2],'pointer':i[3],'accepted':i[4],'wrong':i[5]} for i in d }
	query_list = []
	# print( data )
	
	for handle in handles:
		# t = Thread( target=update_point, args=(handle,) )
		# t.daemon=True
		# t.start()
		# t.join()
		update_point(handle,data,query_list)

	for i in data:
		q1="update score set points={},pointer='{}',accepted={},wrong={} where name='{}'".format(data[i]['points'],data[i]['pointer'],data[i]['accepted'],data[i]['wrong'],i)
		c.execute(q1)

	for i in query_list:
		print(i)	
		c.execute(i)

	query_list=[]

	db.commit()
	db.close()


	
