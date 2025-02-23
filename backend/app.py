from flask import Flask
from flask_cors import CORS
from redis import Redis
from pymongo import MongoClient
from routes import configure_routes
import os

app = Flask(__name__, static_url_path='/static')
CORS(app)

redis = Redis.from_url(os.getenv("REDIS_URL"), ssl_cert_reqs=None)
mongo_client = MongoClient(os.getenv("CONNECTION_STRING"))
mongo_db = mongo_client['SP500_Stocks']

app.config['REDIS'] = redis
app.config['MONGO'] = mongo_db

configure_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
