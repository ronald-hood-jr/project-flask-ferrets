import os
import json
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Linus Torvalds", url=os.getenv("URL"))

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

def get_static_json(path):
    return json.load(open(get_static_file(path)))

def get_static_file(path):
    root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(root, path)
    

