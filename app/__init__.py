from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.app_context().push()
app.config.from_object('config') #secret token to avoid csrf attacks

db = SQLAlchemy(app) #oop[ version of data tables/bases


migrate = Migrate(app, db) # change of models 

from app import views, models
