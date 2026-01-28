from flask import Blueprint, request, render_template, jsonify;
from .database import get_latest_events, save_event
from datetime import datetime

main = Blueprint("main", __name__)

@main.route('/webhook', methods=['POST'])
def webhook():
    pass

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/data')
def fetch_data():
    pass