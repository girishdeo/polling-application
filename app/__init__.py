from flask import Flask
from redis import Redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
redis = Redis(host='localhost', port=6379, db=0)

from app import routes