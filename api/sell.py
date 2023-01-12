from flask import request
from flask_restful import Resource
import yfinance as yf

"""
Sell stock endpoint
/api/sell

  TODO: This endpoint hasn't been implemented yet.
  The following is the documention from the buy endpoint for reference.

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
    stock,
    qty,
  }
"""
class Sell(Resource):
  def post(self):

    return {'message': 'SERVICE_NOT_IMPLEMENTED'}, 501 # not implemented