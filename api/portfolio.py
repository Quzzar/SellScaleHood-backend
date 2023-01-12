from flask import request, jsonify, abort
from flask_restful import Resource
import yfinance as yf

from firebase import portfolio

PORTFOLIO_PAGE_SIZE = 20 # Same as const in constants/data.ts

"""
Portfolio endpoint (given an access_token)
/api/portfolio

returns:
  * 503, SERVICE_OFFLINE - On firebase not being init
  * 400, INVALID_ID_TOKEN - On access_token being invalid
  * 400, INVALID_HEADER - On Authorization header not being correct
  * 200, - On successful retrieval:
    {
      purchases data - TODO: define this object
    }

get:
  headers:
  * Authorization: Bearer <access_token>

  parameters:
  * page (int) - optional
"""
class Portfolio(Resource):
  def get(self):

    try: # Check if properties exist
      bearer_token = request.headers['Authorization']
    except KeyError:
      return {'message': 'INVALID_HEADER'}, 400 # bad request

    if(bearer_token.startswith('Bearer ')):
      bearer_token = bearer_token.replace('Bearer ', '')
    else:
      return {'message': 'INVALID_HEADER'}, 400 # bad request

    page = request.args.get('page', 1, type=int)

    response = portfolio(bearer_token, page, PORTFOLIO_PAGE_SIZE)

    return response