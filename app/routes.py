from flask import Flask,render_template,jsonify,url_for,request
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
	q="select star,name,points,accepted,wrong from score;"
	c.execute(q)
	d = c.fetchall()
	data = [ { 'name':i[1], 'star':i[0], 'points':i[2],'accepted':i[3],'wrong':i[4] } for i in d ]
	db.close()

	data.sort( key=lambda x: x['points'],reverse=True )
	
	data1=[]
	for i in range(len(data)):
		data1.append( ( i+1,data[i] ) )

	return render_template("score.html",data=data1)
	# return jsonify( data )


@app.route("/info/<string:user>")
def info(user):
	db = sq3.connect("score.db")
	c = db.cursor()
	q = "select name,aw,rating,point from aw where name='{}';".format( user )
	c.execute(q)
	d = c.fetchall()
	db.close()
	data = [ { 'name':i[0],'aw':i[1],'rating':i[2],'point':i[3] } for i in d ]
	return render_template("info.html",data=data)

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
		time.sleep(1)


@app.route("/zeta")
def set():
	set_it( handles )
	return "<html><h1>Pointer Seting Done</h1></html>"


