
from flask import Flask, Response
from flask_restful import Api
from flask_cors import CORS
from firebase import init_firebase

from settings import BASE_URL

from api.auth.login import Login
from api.auth.register import Register
from api.auth.refresh import Refresh
from api.auth.info import Info
from api.buy import Buy
from api.sell import Sell
from api.yahoo.query import Query
from api.portfolio import Portfolio
from api.yahoo.trending import Trending
from api.yahoo.top import Top
from api.yahoo.most_watched import MostWatched

app = Flask(__name__)
api = Api(app)
CORS(app,
  origins=[BASE_URL],
  methods=['GET', 'POST'],
  allow_headers=['Authorization', 'Content-Type'],
  allow_methods=['GET', 'POST'],
  supports_credentials=True)

# User account endpoints
api.add_resource(Login, '/api/auth/login/')
api.add_resource(Register, '/api/auth/register/')
api.add_resource(Refresh, '/api/auth/refresh/')
api.add_resource(Info, '/api/auth/info/')

# Stock endpoints
api.add_resource(Buy, '/api/buy/')
api.add_resource(Sell, '/api/sell/')
api.add_resource(Portfolio, '/api/portfolio/')

api.add_resource(Query, '/api/query/')
api.add_resource(Trending, '/api/trending/')
api.add_resource(Top, '/api/top/')
api.add_resource(MostWatched, '/api/most-watched/')

# Fixes CORS issue with flask_restful 
# TODO: there's probably a better way to do this
@app.route('/api/auth/login', methods=['OPTIONS'])
def login_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
@app.route('/api/auth/register', methods=['OPTIONS'])
def register_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
@app.route('/api/auth/info', methods=['OPTIONS'])
def info_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
@app.route('/api/auth/refresh', methods=['OPTIONS'])
def refresh_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
@app.route('/api/buy', methods=['OPTIONS'])
def buy_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
@app.route('/api/sell', methods=['OPTIONS'])
def sell_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response
@app.route('/api/portfolio', methods=['OPTIONS'])
def portfolio_options():
  response = Response()
  response.headers.add('Access-Control-Allow-Methods', 'POST')
  return response

# setup firebase
init_firebase()
  
# driver function
if __name__ == '__main__':
  app.run(debug = True)
