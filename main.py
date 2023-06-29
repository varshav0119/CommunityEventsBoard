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
eventsCollection = db['eventsTest']
usersCollection = db['usersTest']
loggedIn = False

def transform_date(event):
  date = datetime.strptime(event['date'], "%Y-%m-%d")
  event['date'] = date.strftime("%B %d, %Y")
  return event

@app.route('/')
@app.route('/index')
def index():
  global loggedIn
  if not loggedIn:
    return redirect('/choice')
  # homepage with events board
  events = list(eventsCollection.find().sort('date'))
  print(events)
  events = map(transform_date, events)
  return render_template("index.html", events=events)

@app.route('/choice', methods=['GET'])
def choice():
  if request.method == 'GET':
    return render_template("choice.html")

@app.route('/users', methods=['GET'])
def users():
  global loggedIn
  if request.method == 'GET':
    return render_template("login.html")

@app.route('/users/login', methods=['POST'])
def login():
  global loggedIn
  if request.method == 'POST':
    found = usersCollection.find_one({
      'username': request.form['username'],
      'password': request.form['password']
    })
    print(found)
    if found is None:
      return render_template("wrong.html")
    else:
      loggedIn = True
      return redirect("/")

@app.route('/users/logout', methods=['GET'])
def logout():
  global loggedIn
  if request.method == 'GET':
    loggedIn = False
    return redirect("/")

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
  if request.method == 'GET':
    return render_template('register.html')
  if request.method == 'POST':
    usersCollection.insert_one({
      'username': request.form['username'],
      'password': request.form['password']
    })
    return redirect("/")

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
    eventsCollection.insert_one(event)
    return redirect('/')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
