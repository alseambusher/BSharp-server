from app import app
from pymongo import MongoClient
from datetime import datetime
from flask import request
from flask import render_template
import scipy.spatial as sp
import numpy as np
import heapq

client = MongoClient()
db = client.test

def cosine_sim(song1,song2):
    sim = 1 - sp.distance.cosine(song1,song2)
    return np.sum(sim)   

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def publishSong():
	"""	
	songList = (db.songs.find({}, {song:1, _id:1})).toArray()
	print(songList)
	similarity_values = []
	for i in range(len(songs)):
        	minL = min(len(currSong),len(songs[i]))
    		similarity_values.append(cosine_sim(currSong[0:minL],songs[i][0:minL]))
	heapq.nlargest(3, range(len(songs)),songs.__getitem__)

	curl --data "[1,2,34,31]" localhost:8000/store?timestamp=12345&songname=abcd&artist=yash&price=1 -XPOST
	"""
	print(request.args.get('songname'))
	timestamp = request.args.get('timestamp')	
	song = request.data
	songname = request.args.get('songname')	
	artist = request.args.get('artist')
	price = request.args.get('price')
	result = db.songs.insert_one({ "timestamp" : timestamp,
				      "artist" : artist,
					"price": price,
					"song" : song,
					"songname" : songname					
					})
	return "Done"
	"""
	return "Done"
	"""
@app.route('/store', methods=['GET'])
def getSongs():
	return str([x for x in db.songs.find()])
	
@app.route('/store/<songname>', methods=['GET'])
def getSong(songname):
	return [x for x in db.songs.find({"songname":songname})]




