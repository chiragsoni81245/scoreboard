
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from threading import Thread
import sqlite3 as sq3


def set_pointer( handle ):

	r = requests.get("https://codeforces.com/submissions/{}/page/1".format(handle))
	soup = BeautifulSoup(r.text,"html.parser")
	table = soup.find_all("table",{"class":["status-frame-datatable"]})[0]
	pointer = table.find_all("tr")[1].find_all("td")[0].text.strip().strip("\n")
	db = sq3.connect("score.db")
	c = db.cursor()
	q = "update score set pointer='{}' where name='{}';".format( pointer, handle )
	c.execute(q)
	db.commit()
	db.close()

def set_it( handles ):

	for handle in handles:
		# t = Thread( target=set_pointer, args=( handle, ) )
		# t.daemon = True
		# t.start()
		# t.join()
		set_pointer( handle )

