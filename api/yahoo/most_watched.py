from flask import request
from flask_restful import Resource
import yfinance as yf
from yahooquery import Screener
from utils import get_basic_info

"""
Most watched stocks endpoint
/api/most-watched

get:
  parameters:
  * count (int) - required
"""
class MostWatched(Resource):
  s = Screener()

  def get(self):

    count = request.args.get('count', 10, type=int)

    data = self.s.get_screeners(['most_watched_tickers'], count)
    most_watched = [x['symbol'] for x in data['most_watched_tickers']['quotes']]

    most_watched_info = [get_basic_info(x.info) for x in yf.Tickers(most_watched).tickers.values()]

    return {
      'message': '',
      'data': most_watched_info,
    }, 200 # okay

