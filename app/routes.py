from flask import Blueprint, request, render_template, jsonify;
from .database import get_latest_events, save_event
from datetime import datetime, timezone

main = Blueprint("main", __name__)

@main.route('/webhook', methods=['POST'])
def webhook():
    print("WEBHOOK RECEIVED")
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    event_document = {}

    try:
        if event_type == 'push':
            event_document = {
                "request_id" : data["after"],
                "author" : data['pusher']['name'],
                "action" : "PUSH",
                "from_branch" : "",
                "to_branch" : data['ref'].split('/')[-1],
                "timestamp" : datetime.now(timezone.utc).isoformat()
            }
        elif event_type == 'pull_request':
            action_type = 'MERGE' if data['pull_request']['merged'] else 'PULL_REQUEST'
            event_document = {
                "request_id" : str(data['pull_request']['id']), 
                "author" : data['pull_request']['user']['login'],
                "action" : action_type,
                "from_branch" : data['pull_request']['head']['ref'],
                "to_branch" : data['pull_request']['base']['ref'],
                "timestamp" : datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        print("ERROR CREATING EVENT DOCUMENT:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

    if event_document:
        save_event(event_document)
        print("SAVED TO MONGO:", event_document)
        return jsonify({"status": "success"}), 200
    else:
        print("No event_document created")
        return jsonify({"status": "ignored"}), 200

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/data')
def fetch_data():
    events = get_latest_events()

    messages = []

    for e in events:
        if e['action'] == 'PUSH':
            message = f"\"{e['author']}\" pushed to \"{e['to_branch']}\" on {e['timestamp']} UTC"
        elif e['action'] == 'PULL_REQUEST':
            message = f"\"{e['author']}\" submitted a pull request from {e['from_branch']} to {e['to_branch']} on {e['timestamp']} UTC"
        elif e['action'] == 'MERGE':
            message = f"\"{e['author']}\" merged branch {e['from_branch']} to {e['to_branch']} on {e['timestamp']} UTC"
        messages.append(message)

    return jsonify(messages)