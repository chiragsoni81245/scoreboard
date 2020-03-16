import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from threading import Thread
import sqlite3 as sq3

# AW = Accepted Wrong
def func_points(handle,rating,data,AW):

	if data[handle]["star"] == 4:
		if rating < 1100:
			if AW==True:
				data[handle]["points"] += 30
			else:
				data[handle]["points"] -= 6				
		elif rating > 1400:
			if AW==True:
				data[handle]["points"] += 100
			else:
				data[handle]["points"] -= 20
		else:
			if AW==True:
				data[handle]["points"] += ((rating-1100)/100)*10+50
			else:
				data[handle]["points"] -= (((rating-1100)/100)*10+50)//5				

	if data[handle]["star"] == 3:
		if rating < 1000:
			if AW==True:
				data[handle]["points"] += 30
			else:
				data[handle]["points"] -= 6	
		elif rating > 1200:
			if AW==True:
				data[handle]["points"] += 100
			else:
				data[handle]["points"] -= 20
		else:
			if AW==True:
				data[handle]["points"] += ((rating-1000)/100)*25+50
			else:
				data[handle]["points"] -= (((rating-1000)/100)*25+50)//5				

	if data[handle]["star"] == 2:
		if rating < 900:
			if AW==True:
				data[handle]["points"] += 30
			else:
				data[handle]["points"] -= 6	
		elif rating > 1100:
			if AW==True:
				data[handle]["points"] += 100
			else:
				data[handle]["points"] -= 20

		else:
			if AW==True:
				data[handle]["points"] += ((rating-900)/100)*25+50
			else:
				data[handle]["points"] -= (((rating-900)/100)*25+50)//5				

	if data[handle]["star"] == 1:
		if rating < 700:
			if AW==True:
				data[handle]["points"] += 30
			else:
				data[handle]["points"] -= 6	
		elif rating > 900:
			if AW==True:
				data[handle]["points"] += 100
			else:
				data[handle]["points"] -= 20
		else:
			if AW==True:
				data[handle]["points"] += ((rating-700)/100)*25+50
			else:
				data[handle]["points"] -= (((rating-700)/100)*25+50)//5

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
	# print(r.text)
	# print(soup.prettify())
	table = soup.find_all("table",{"class":["status-frame-datatable"]})[0]
	# print(table)
	trs = table.find_all("tr")[1:]

	c = 0
	w = 0
	accepted = []
	wrong = []
	br=0
	fp = trs[0].find_all("td")[0].text.strip().strip("\n")
	for i in trs:
		point = i.find_all("td")[0].text.strip()

		if point == data[handle]["pointer"]:
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
						accepted.append( rating )
				else:
					w = w + 1
					link = "https://codeforces.com"+i.find_all("td")[3].a['href']
					rating = fetch_rating(link)
					if rating!=-1:
						wrong.append( rating )
		except:
			pass
			
	data[handle]["pointer"] = fp
	return  [ [c,w,accepted,wrong], br ]

def page_traversal(handle,data):
	page=1
	c,w,accepted,wrong=0,0,[],[]
	while(1):
		result = get_questions( handle,page,data )

		l=result[0]
		c+=l[0]
		w+=l[1]
		accepted+=l[2]
		wrong+=l[3]

		if result[1]==1:
			break

		page+=1

	for i in accepted:
		func_points(handle,i,data,True)

	for i in wrong:
		func_points( handle,i,data,False )

	print( "{} Accepted:{}, Wrong:{}, Points:{}".format( handle, c,w, data[handle]['points'] ) )

def update_point( handle,data ):
	page_traversal(handle,data)

def score_count( handles ):
	db = sq3.connect("score.db")
	c = db.cursor()
	q="select star,name,points,pointer from score;"
	c.execute(q)
	d = c.fetchall()
	data = defaultdict(dict)
	data = { i[1]:{'star':i[0],'points':i[2],'pointer':i[3]} for i in d }
	# print( data )
	
	for handle in handles:
		# t = Thread( target=update_point, args=(handle,) )
		# t.daemon=True
		# t.start()
		# t.join()
		update_point(handle,data)

	for i in data:
		q1="update score set points={},pointer='{}' where name='{}'".format(data[i]['points'],data[i]['pointer'],i)
		c.execute(q1)

	db.commit()
	db.close()


	
