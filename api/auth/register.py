from flask import request, jsonify, abort
from flask_restful import Resource

from firebase import register

"""
Register endpoint for user (given an email and password)
/api/auth/register

returns:
  * 503, SERVICE_OFFLINE - On firebase not being init
  * 400, EMAIL_EXISTS - On user email already being registered
  * 201, - On successful register:
    {
    }

post:
  body (json):
  {
    email,
    password,
    displayName,
  }
"""
class Register(Resource):
  def post(self):
    request_data = request.get_json()

    try: # Check if properties exist
      email = request_data['email']
      password = request_data['password']
      displayName = request_data['displayName']
    except KeyError:
      return {'message': 'INVALID_BODY'}, 400 # bad request

    response = register(email, password, displayName)

    return response