from flask import Flask, render_template
from dotenv import load_dotenv
import os
from flask_cors import CORS
from config.mongodb import mongo
from routes.users_routes import users
from routes.courses_routes import courses  

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(courses, url_prefix='/courses')  

if __name__ == '__main__':
    app.run(debug=True)
