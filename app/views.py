from app import app
from pymongo import MongoClient
from datetime import datetime
from flask import request
from flask import render_template
import scipy.spatial as sp
import numpy as np
import heapq
import json
import ast

client = MongoClient()
db = client.test

def cosine_sim(song1,song2):
    print(song1,song2)
    sim = 1 - sp.distance.cosine(song1,song2)
    return np.sum(sim)   

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def publishSong():
	songList = list(db.songs.find({}, {"song": 1, "_id": 1}))
	songs = map(lambda x: json.loads(str(x["song"])), songList)
	
	currSong = ast.literal_eval(request.data)
	similarity_values = []
	for song in songs:
		song = ast.literal_eval(str(song))
		minL = min(len(currSong),len(song))
    		similarity_values.append(cosine_sim(currSong[0:minL],song[0:minL]))
	sim = heapq.nlargest(3, range(len(songList)))
	print(sim)
	
	timestamp = request.args.get('timestamp')	
	result = db.songs.insert_one({ "timestamp" : "$currentDate",
					"song" : currSong,
					"similar": sim
					})
	return "Done"
	
@app.route('/store', methods=['GET'])
def getSongs():
	return json.dumps([x for x in db.songs.find({}, {"song":1, "timestamp": 1, "_id":0})])
	
@app.route('/store/<songname>', methods=['GET'])
def getSong(songname):
	return json.dumps([x for x in db.songs.find({"songname":songname})])

@app.route('/store' , methods=['DELETE'])
def deleteAll():
	db.songs.remove()
	return "Deleted"

