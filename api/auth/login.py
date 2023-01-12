from flask import request
from flask_restful import Resource

from firebase import signin

"""
Login endpoint for user (given an email and password)
/api/auth/login

returns:
  * 503, SERVICE_OFFLINE - On firebase not being init
  * 403, EMAIL_NOT_VERIFIED - On user email needing to be verified
  * 400, EMAIL_NOT_FOUND - On user email not existing in system
  * 400, INVALID_EMAIL - On user email not being correct
  * 400, INVALID_PASSWORD - On user password not being correct
  * 200, - On successful login:
    {
      localId,
      email,
      displayName,
      accessToken,
      refreshToken,
    }


post:
  body (json):
  {
    email,
    password
  }
"""
class Login(Resource):
  def post(self):
    request_data = request.get_json()

    try: # Check if properties exist
      email = request_data['email']
      password = request_data['password']
    except KeyError:
      return {'message': 'INVALID_BODY'}, 400 # bad request

    response = signin(email, password)

    return response