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
from bson import json_util
import time
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
	current = map(lambda x: x[1], currSong)    	
	similarity_values = []
	for song in songs:
		song = map(lambda x: x[1] , ast.literal_eval(str(song)))
		minL = min(len(current),len(song))
		similarity_values.append(cosine_sim(current[0:minL],song[0:minL]))
	sim = heapq.nlargest(5, range(len(songs)))
	sim = [songs[i] for i in sim]
	result = db.songs.insert_one({"song": currSong,"similar": sim , "timestamp": time.time()})
	return "Done"

@app.route('/fixDB',methods=['GET'])
def fixDB():
	songList = list(db.songs.find({}, {"song": 1, "_id": 1}))
	songs = map(lambda x: json.loads(str(x["song"])), songList)
	for originalsong in songs:
		tsong1 = map(lambda x: x[1] , ast.literal_eval(str(originalsong))) 	
		similarity_values = []
		for song2 in songs:
			tsong2 = map(lambda x: x[1] , ast.literal_eval(str(song2)))
			print("tsong1:",tsong1,tsong2)			
			if(tsong1 == tsong2):
				continue
			minL = min(len(tsong1),len(tsong2))
			similarity_values.append(cosine_sim(tsong1[0:minL],tsong2[0:minL]))
		sim = heapq.nlargest(5, range(len(songs)))
		sim = [songs[i] for i in sim]
		result = db.songs.insert_one({"song": originalsong,"similar": sim , "timestamp": time.time()})
	return "Done"
@app.route('/store', methods=['GET'])
def getSongs():
	return json.dumps([x for x in db.songs.find({}, {"song":1,'timestamp': 1,"similar":1 ,"_id":0})], default=json_util.default)
	
@app.route('/store/<songname>', methods=['GET'])
def getSong(songname):
	return json.dumps([x for x in db.songs.find({"songname":songname})])

@app.route('/store' , methods=['DELETE'])
def deleteAll():
	db.songs.remove()
	return "Deleted"

@app.route('/recommend', methods=['POST'])
def recommend():
	song = ast.literal_eval(request.data)
	mySongs = list(db.songs.find({"song": song}, {"song":1, "timestamp": 1,"sim":1, "_id":0}))
	recommendations = map(lambda x: json.loads(x["similar"]),mySongs)
	return recommendations
	

