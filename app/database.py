from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['github_events_db']
collection = db['events']

def save_event(data):
    collection.insert_one(data)

def get_latest_events():
    return list(collection.find().sort("timestamp", -1).limit(10))