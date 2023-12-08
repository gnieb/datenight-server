from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api


load_dotenv()
app = Flask(__name__)
api = Api(app)

