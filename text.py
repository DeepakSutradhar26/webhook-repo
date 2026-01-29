from app.database import collection

events = list(collection.find())
for e in events:
    print(e)
