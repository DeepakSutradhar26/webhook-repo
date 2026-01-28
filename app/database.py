from pymongo import MongoClient

client = MongoClient("mongodb+srv://<netninja>:<6vmKpPM7dXMHAyKQ>@clusterdata.wzwkvne.mongodb.net/?appName=ClusterData")
db = client['github_events_db']
collection = db['events']

def save_event(data):
    collection.insert_one(data)

def get_latest_events():
    return list(collection.find().sort("timestamp", -1).limit(10))