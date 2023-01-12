
def get_basic_info(stock_info: dict):
  if stock_info is None:
    return None
  
  if stock_info.get('currentPrice') is not None and stock_info.get('previousClose') is not None:
    dayChange = stock_info.get('currentPrice') - stock_info.get('previousClose')
    dayPercent = (100 / stock_info.get('currentPrice')) * dayChange
  else:
    dayChange = None
    dayPercent = None

  return {
    'name': stock_info.get('shortName') or stock_info.get('longName') or stock_info.get('symbol') or '',
    'summary': stock_info.get('longBusinessSummary') or '',
    'sector': stock_info.get('sector') or 'Unknown',
    'ticker': stock_info.get('symbol'),
    'trend': 'down' if dayChange is not None and dayChange < 0 else 'up',
    'price': stock_info.get('currentPrice'),
    'dayChange': dayChange,
    'dayPercent': dayPercent,
  }