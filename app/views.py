from app import app
from pymongo import MongoClient
from datetime import datetime
from flask import request
client = MongoClient()
db = client.test
@app.route('/')
def index():
    db.songs.remove({})
    return "Hello, World!"

@app.route('/store', methods=['POST'])
def publishSong():
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
	return result.inserted_id
@app.route('/store', methods=['GET'])
def getSongs():
	return [x for x in db.songs.find()]
	
@app.route('/store/<songname>', methods=['GET'])
def getSong(songname):
	return [x for x in db.songs.find({"songname":songname})]




