
import json
import pyrebase
from settings import FIREBASE_CONFIG

def init_firebase():
  global auth
  global db

  firebase = pyrebase.initialize_app(FIREBASE_CONFIG)

  # Get a reference to the auth service
  auth = firebase.auth()

  # Get a reference to the database service
  db = firebase.database()


"""
Login workflow

Returns:
* 503, SERVICE_OFFLINE - On firebase not being init
* 403, EMAIL_NOT_VERIFIED - On user email needing to be verified
* 400, EMAIL_NOT_FOUND - On user email not existing in system
* 400, INVALID_EMAIL - On user email not being correct
* 400, INVALID_PASSWORD - On user password not being correct
* 200, - On successful login
"""
def signin(email, password):
  try:
    auth
  except NameError:
    print('Firebase has not been initialized!')
    return {'message': 'SERVICE_OFFLINE'}, 503 # service unavailable

  try:
    user = auth.sign_in_with_email_and_password(email, password)
  except Exception as e: # An alternative to this would be using the 'firebase_admin' package
    return {'message': json.loads(e.args[1])['error']['message']}, json.loads(e.args[1])['error']['code']
    
  user_info = auth.get_account_info(user['idToken'])

  # Check if the user is email verified,
  if(not user_info['users'][0]['emailVerified']):
    return {'message': 'EMAIL_NOT_VERIFIED'}, 403 # forbidden

  headers = [
    # If we wanted to use cookies instead of localStorage
    #('Set-Cookie', 'accessToken={}'.format(user['idToken'])),
    #('Set-Cookie', 'refreshToken={}'.format(user['refreshToken']))
  ]
  return {
    'message': '',
    'data': {
      'localId': user_info['users'][0].get('localId'),
      'email': user_info['users'][0].get('email'),
      'displayName': user_info['users'][0].get('displayName'),
      'accessToken': user['idToken'],
      'refreshToken': user['refreshToken'],
    },
  }, 200, headers


"""
Register workflow

Returns:
* 503, SERVICE_OFFLINE - On firebase not being init
* 400, EMAIL_EXISTS - On user email already being registered
* 201, - On successful register
"""
def register(email, password, displayName=None):
  try:
    auth
  except NameError:
    print('Firebase has not been initialized!')
    return {'message': 'SERVICE_OFFLINE'}, 503 # service unavailable

  try:
    user = auth.create_user_with_email_and_password(email, password)
  except Exception as e: # An alternative to this would be using the 'firebase_admin' package
    return {'message': json.loads(e.args[1])['error']['message']}, json.loads(e.args[1])['error']['code']

  if displayName:
    auth.update_profile(user['idToken'], displayName)

  auth.send_email_verification(user['idToken'])

  headers = []
  return {'message': ''}, 201, headers # created


"""
Refresh access token workflow

Returns:
* 503, SERVICE_OFFLINE - On firebase not being init
* 400, INVALID_REFRESH_TOKEN - On refresh token not being valid
* 201, - On successful refresh
"""
def refreshToken(refreshToken):
  try:
    auth
  except NameError:
    print('Firebase has not been initialized!')
    return {'message': 'SERVICE_OFFLINE'}, 503 # service unavailable

  try:
    user = auth.refresh(refreshToken)
  except Exception as e: # An alternative to this would be using the 'firebase_admin' package
    return {'message': json.loads(e.args[1])['error']['message']}, json.loads(e.args[1])['error']['code']

  headers = [
    # If we wanted to use cookies instead of localStorage
    #('Set-Cookie', 'accessToken={}'.format(user['idToken'])),
    #('Set-Cookie', 'refreshToken={}'.format(user['refreshToken']))
  ]
  return {
    'message': '',
    'data': {
      'accessToken': user['idToken'],
      'refreshToken': user['refreshToken'],
    },
  }, 201, headers # created


"""
Stock purchase workflow

Returns:
* 503, SERVICE_OFFLINE - On firebase not being init
* 400, INVALID_ID_TOKEN - On user idToken being invalid
* 200, - On successful purchase
"""
def purchase(idToken, ticker, qty, price):
  try:
    db
    auth
  except NameError:
    print('Firebase has not been initialized!')
    return {'message': 'SERVICE_OFFLINE'}, 503 # service unavailable
  
  try:
    user_info = auth.get_account_info(idToken)
  except Exception as e: # An alternative to this would be using the 'firebase_admin' package
    return {'message': json.loads(e.args[1])['error']['message']}, json.loads(e.args[1])['error']['code']

  localId = user_info['users'][0]['localId']

  db.child('users').child(localId).child('purchases').push({
    'ticker': ticker,
    'qty': qty,
    'price': price,
  })

  return {
    'message': '',
    'data': {
      'ticker': ticker,
      'qty': qty,
      'price': price,
    },
  }, 200 # okay


"""
Portfolio retrieval workflow

Returns:
* 503, SERVICE_OFFLINE - On firebase not being init
* 400, INVALID_ID_TOKEN - On user idToken being invalid
* 200, - On successful retrieval
"""
def portfolio(idToken, page, pageSize):
  try:
    db
    auth
  except NameError:
    print('Firebase has not been initialized!')
    return {'message': 'SERVICE_OFFLINE'}, 503 # service unavailable

  try:
    user_info = auth.get_account_info(idToken)
  except Exception as e: # An alternative to this would be using the 'firebase_admin' package
    return {'message': json.loads(e.args[1])['error']['message']}, json.loads(e.args[1])['error']['code']

  localId = user_info['users'][0]['localId']

  # TODO: Limit the queried data to page and pageSize (and sort it here maybe?)
  purchases = db.child('users').child(localId).child('purchases').get()

  return {
    'message': '',
    'data': purchases.val(),
  }, 200 # okay


"""
Info retrieval workflow

Returns:
* 503, SERVICE_OFFLINE - On firebase not being init
* 400, INVALID_ID_TOKEN - On user idToken being invalid
* 200, - On successful retrieval
"""
def info(idToken):
  try:
    auth
  except NameError:
    print('Firebase has not been initialized!')
    return {'message': 'SERVICE_OFFLINE'}, 503 # service unavailable

  try:
    user_info = auth.get_account_info(idToken)
  except Exception as e: # An alternative to this would be using the 'firebase_admin' package
    return {'message': json.loads(e.args[1])['error']['message']}, json.loads(e.args[1])['error']['code']

  return {
    'message': '',
    'data': {
      'localId': user_info['users'][0].get('localId'),
      'email': user_info['users'][0].get('email'),
      'displayName': user_info['users'][0].get('displayName'),
    },
  }, 200 # okay
