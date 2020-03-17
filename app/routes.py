from flask import Flask,render_template,jsonify,url_for,request
from app.set_pointer import *
from app.utility_function import *
from collections import OrderedDict
import time
from app import app
from datetime import datetime
from multiprocessing import Process
import multiprocessing
from threading import Thread
import threading
from datetime import datetime

handles = ['hr4_harsh', 'ziddi', 'tanu38', 'chiragsoni812', 'mohi07', 'chauhan002', 'shivambhat', 'sp_', 'Nishant_Rao', 'Aka_coder', 'AM_coder', 'ankitkochar1578', '_viru_', 'hitzmac', 'khiladi.07', '_chanchal', "shubhamz950"]

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
	q = "select name,aw,rating,point,question_txt,question_link,date_time from aw where name='{}';".format( user )
	c.execute(q)
	d = c.fetchall()
	db.close()
	data = [ { 'aw':i[1],'rating':i[2],'point':i[3],"question_txt":i[4],"question_link":i[5],"date_time":i[6] } for i in d ]
	data.sort( key=lambda x: datetime.strptime( x['date_time'],"%b/%d/%Y %H:%M" ),reverse=True )
	return render_template("info.html",data=data,name=user)

@app.route("/alpha")
def reload():
	flag=0
	for i in threading.enumerate():
		if i.name=="reloader":
			flag=1
	if flag==1:
		return "<html><h1>Already Running</h1></html>"
	else:
		# Thread(name="reloader",target=reloading,args=(handles,)).start()
		Thread(name="reloader",target=reloading,args=(handles,)).start()
		return "<html><h1>Reloading Started</h1></html>"

@app.route("/salpha")
def stop_reload():
	flag=0
	for i in threading.enumerate():
		if i.name=="reloader":
			flag=1
			i.terminate()
	if flag==1:
		return "<html><h1>Reloader Stoped</h1></html>"
	else:
		return "<html><h1>Roloader is already stoped</h1></html>"

@app.route("/status_reloader")
def status_reloader():
	flag=0
	for i in threading.enumerate():
		if i.name=="reloader":
			flag=1
	if flag==1:
		return "<html><h1>Running</h1></html>"
	else:
		return "<html><h1>Not Running</h1></html>"

def reloading(handles):
	while True:
		print("\nReloading has been started [{}]\n\n".format( datetime.now().strftime("%Y-%m-%d %H:%M") ) )
		score_count( handles )
		time.sleep(2)

@app.route("/sudo_reload")
def sudo_reload():
	score_count( handles )
	return "<html><h1>Reloading Complete and reloader started again</h1></html>"


@app.route("/zeta")
def set():
	set_it( handles )
	return "<html><h1>Pointer Seting Done</h1></html>"


