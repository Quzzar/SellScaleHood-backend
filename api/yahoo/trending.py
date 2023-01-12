from flask import request
from flask_restful import Resource
import yfinance as yf
from yahooquery import Screener
from utils import get_basic_info

"""
Trending stocks endpoint
/api/trending

get:
  parameters:
  * count (int) - required
"""
class Trending(Resource):
  s = Screener()

  def get(self):

    count = request.args.get('count', 10, type=int)

    data = self.s.get_screeners(['day_gainers'], count)
    day_gainers = [x['symbol'] for x in data['day_gainers']['quotes']]

    day_gainers_info = [get_basic_info(x.info) for x in yf.Tickers(day_gainers).tickers.values()]

    return {
      'message': '',
      'data': day_gainers_info,
    }, 200 # okay

