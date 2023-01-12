from flask import request
from flask_restful import Resource
import yfinance as yf
from utils import get_basic_info

"""
Query stock endpoint
/api/query

returns:
  * 404, STOCK_NOT_FOUND - On stock not being found
  * 200, - On successful stock query:
    {
      depends on details parameter
    }

get:
  parameters:
  * ticker (str) - required
  * details (boolean) - optional
"""
class Query(Resource):
  def get(self):

    ticker = request.args.get('ticker', '', type=str)
    details = request.args.get('details', 'false', type=str)

    msft = yf.Ticker(ticker)

    if(msft.info is None):
      return {'message': 'STOCK_NOT_FOUND'}, 404 # not found

    return {
      'message': '',
      'data': msft.info if details == 'true' else get_basic_info(msft.info),
    }, 200 # okay