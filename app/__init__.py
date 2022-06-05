import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/hobbies')
def hobbies():
    my_hobbies = ["hiking", "skiing", "kayaking", "skating", "snowboarding", "painting", "watching movies", "reading"]
    return render_template('hobbies.html', my_hobbies=my_hobbies)

@app.route('/experiences')
def experiences():
    return render_template('experiences.html')



