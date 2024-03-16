from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail
from flask_socketio import SocketIO,emit
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Flask Mail config #
app.config['MAIL_SERVER']=os.getenv('MAIL_SMTP')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


db = SQLAlchemy()
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
db.init_app(app)
CORS(app,resources={r"/*":{"origins":"*"}})

socketio = SocketIO(app,cors_allowed_origins="*")



