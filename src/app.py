from flask import Flask, render_template #Import the Flask class from the flask module
from dotenv import load_dotenv # Import the load_dotenv function from the dotenv module
import os # Import the os module
from flask_cors import CORS  # Importa Flask-CORS
from config.mongodb import mongo # Import the mongo object from the mongodb module
from routes.users_routes import users # Import the users object from the users_routes module

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(users, url_prefix='/users')



if __name__ == '__main__':
    app.run(debug=True)