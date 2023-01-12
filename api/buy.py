from flask import request
from flask_restful import Resource
import yfinance as yf

from firebase import purchase

"""
Buy stock endpoint
/api/buy

returns:
  * 503, SERVICE_OFFLINE - On firebase not being init
  * 400, INVALID_ID_TOKEN - On access_token being invalid
  * 400, INVALID_HEADER - On Authorization header not being correct
  * 400, INVALID_BODY - On body not including stock and qty
  * 400, QTY_NOT_VALID - On qty not being an integer
  * 404, STOCK_NOT_FOUND - On stock not being found
  * 200, - On successful purchase:
    {
      stock,
      qty,
      price,
    }

post:
  headers:
  * Authorization: Bearer <access_token>

  body (json):
  {
    ticker,
    qty,
  }
"""
class Buy(Resource):
  def post(self):
    request_data = request.get_json()

    try: # Check if header exist
      bearer_token = request.headers['Authorization']
    except KeyError:
      return {'message': 'INVALID_HEADER'}, 400 # bad request

    if(bearer_token.startswith('Bearer ')):
      bearer_token = bearer_token.replace('Bearer ', '')
    else:
      return {'message': 'INVALID_HEADER'}, 400 # bad request

    try: # Check if properties exist
      ticker = request_data['ticker']
      qty = request_data['qty']
    except KeyError:
      return {'message': 'INVALID_BODY'}, 400 # bad request

    # Check if qty is an integer
    if(not isinstance(qty, int)):
      return {'message': 'QTY_NOT_VALID'}, 400 # bad request

    msft = yf.Ticker(ticker)

    print(msft.info) # make the stock the symbol

    if(msft.info is None):
      return {'message': 'STOCK_NOT_FOUND'}, 404 # not found

    # TODO: In reality, the price wouldn't just be the current. It's much more complicated than that.
    response = purchase(bearer_token, ticker, qty, msft.info['currentPrice'])

    return response