from flask import Flask
from models import db
from views import views
from dotenv import load_dotenv
import os

#### Load environment variables from .env file ####
load_dotenv()

#### Initialize Flask app ####
app = Flask(__name__)

##### Use the DATABASE_URL from the .env file ######
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

##### Create all tables #####
with app.app_context():
    db.create_all()

##### Register the views blueprint #####
app.register_blueprint(views)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
