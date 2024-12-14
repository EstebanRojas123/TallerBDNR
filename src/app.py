from flask import Flask, jsonify
from neo4j import GraphDatabase
from flask import request
import datetime 
from flask import Flask, render_template
from dotenv import load_dotenv
import os
from flask_cors import CORS
from config.mongodb import mongo
from config.initialize_db import initialize_database
from routes.users_routes import users
from routes.courses_routes import courses 
from routes.units_routes import units
from routes.class_routes import classes
from poblar_db import populate_database
from routes.dynamodb_routes import dynamodb_bp
from routes.neo4j_routes import neo4j_bp
import requests

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)
CORS(app)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(neo4j_bp, url_prefix='/neo4j')
app.register_blueprint(dynamodb_bp, url_prefix='/dynamodb')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(courses, url_prefix='/courses') 
app.register_blueprint(units, url_prefix='/units')
app.register_blueprint(classes, url_prefix='/classes')

if __name__ == '__main__':
    app.run(debug=True)
