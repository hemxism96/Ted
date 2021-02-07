#This file intializes a Python module. 
#Without it, Python will not recognize the app directory as a module.

from flask import Flask
#from flask_bootstrap import Bootstrap
from pymongo import MongoClient

#initialize the app
app=Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY']='ted'

#Bootstrap(app)

#configuration
#app.config.from_object('config') #name of config file

#database
client=MongoClient()
db=client.ted.ted_videos

#Load the views and models
from app import views
