# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os
from datetime import datetime

# -- Initialization section --
app = Flask(__name__)

## Set your password as a secret env variable
password = os.environ['official_password']

## Set up URI of database as a "client"
client = MongoClient(
  f"mongodb+srv://admin:{password}@randomcluster.jzdwwkv.mongodb.net/?retryWrites=true&w=majority"
)

db = client['database']
collection = db['eventsTest']


def transform_date(event):
  date = datetime.strptime(event['date'], "%Y-%m-%d")
  event['date'] = date.strftime("%B %d, %Y")
  return event


@app.route('/')
@app.route('/index')
def index():
  # homepage with events board
  events = list(collection.find().sort('date'))
  print(events)
  events = map(transform_date, events)
  return render_template("index.html", events=events)


@app.route('/events/new', methods=['POST', 'GET'])
def new_events():
  if request.method == 'GET':
    return render_template('new_event.html')
  else:
    event = {
      'event': request.form['event_name'],
      'date': request.form['event_date']
    }
    print(event)
    collection.insert_one(event)
    return redirect('/')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
