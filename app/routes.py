from flask import Flask,render_template,jsonify
from app.set_pointer import *
from app.utility_function import *
from collections import OrderedDict
from threading import Thread
import time
from app import app

handles = ['ziddi', 'tanu38', 'chiragsoni812', 'mohi07', 'chauhan002', 'shivambhat', 'sp_', 'Nishant_Rao', 'Aka_coder', 'hr4_harsh', 'AM_coder', 'ankitkochar1578', '_viru_', 'hitzmac', 'khiladi.07', '_chanchal', "shubhamz950"]

@app.route("/")
def index():
		
	db = sq3.connect("score.db")
	c = db.cursor()
	q="select star,name,points,pointer from score;"
	c.execute(q)
	d = c.fetchall()
	data = [ { 'name':i[1], 'star':i[0], 'points':i[2] } for i in d ]
	db.close()

	data.sort( key=lambda x: x['points'],reverse=True )
	return render_template("score.html",data=data)
	# return jsonify( data )

@app.route("/alpha")
def reload():
	t = Thread(target=reloading,args=(handles,))
	t.start()
	return "<html><h1>Reloading Started ( complete in 2 minutes ) </h1></html>"


def reloading(handles):
	print("Thread has been started")
	while(True):
		score_count( handles )
		print("reloaded")
		time.sleep(1*60)


@app.route("/zeta")
def set():
	set_it( handles )
	return "<html><h1>Pointer Seting Done</h1></html>"


