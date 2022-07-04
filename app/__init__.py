import os
import json
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import requests
from requests.structures import CaseInsensitiveDict
from flask_assets import Bundle, Environment
url = "http://localhost:5000/api/timeline_post"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

load_dotenv()
app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

if os.getenv('TESTING') == 'true':
    print('Running in test mode')
    mydb = SqliteDatabase ('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306)

print(mydb)


@app.route('/')
def index():
    return render_template('index.html', title="Linus Torvalds", url=os.getenv("URL"))

@app.route('/tailwind')
def tailwind():
    return render_template('tailwind.html')

@app.route('/education')
def education():
    education = get_static_json("static/files/education.json")
    return render_template('education.html', education=education)

@app.route('/hobbies')
def hobbies():
    my_hobbies = ["hiking", "skiing", "kayaking", "skating", "snowboarding", "painting", "watching movies", "reading"]
    return render_template('hobbies.html', my_hobbies=my_hobbies)

@app.route('/experiences')
def experiences():
    experiences = get_static_json("static/files/experiences.json")
    return render_template('experiences.html', experiences=experiences)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if name == '' or name is None:
        return 'Invalid name', 400
    elif content == '' or content is None:
        return 'Invalid content', 400
    elif email == '' or email is None or '@' not in email:
        return 'Invalid email', 400
    else:
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/timeline')
def timeline():
    
    timeline = {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
    return render_template('timeline.html', timeline=timeline)

def createJSON():
    resp = "h"
    f = open("static/files/timeline.json", "w")
    f.write(resp)
    f.close()

def get_static_json(path):
    return json.load(open(get_static_file(path)))

def get_static_file(path):
    root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(root, path)
    

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])