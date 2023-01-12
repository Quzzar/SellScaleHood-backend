from flask import request
from flask_restful import Resource
import yfinance as yf
from yahooquery import Screener
from utils import get_basic_info

"""
Top stocks endpoint
/api/top

get:
  parameters:
  * count (int) - required
"""
class Top(Resource):
  s = Screener()

  def get(self):

    count = request.args.get('count', 10, type=int)

    data = self.s.get_screeners(['most_actives'], count)
    most_actives = [x['symbol'] for x in data['most_actives']['quotes']]

    most_actives_info = [get_basic_info(x.info) for x in yf.Tickers(most_actives).tickers.values()]

    return {
      'message': '',
      'data': most_actives_info,
    }, 200 # okay

