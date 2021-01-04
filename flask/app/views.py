#This file contains all the routes for our application. 
#This will tell Flask what to display on which path.

from . import db
from app import app
from flask import render_template

@app.route('/')
def hello():
    return 'Hello Ted World'

@app.route('/ted_videos',methods=['GET', 'POST'])
def ted_videos():
    ted_video=db.find()
    return render_template('ted.html',videos=ted_video)