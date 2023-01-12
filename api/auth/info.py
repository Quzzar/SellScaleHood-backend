from flask import request
from flask_restful import Resource

from firebase import info

"""
Get user info endpoint
/api/auth/info

returns:
  * 400, INVALID_HEADER - On Authorization header not existing
  * 503, SERVICE_OFFLINE - On firebase not being init
  * 400, INVALID_ID_TOKEN - On user idToken being invalid
  * 200, - On successful retrieval:
    {
      localId,
      email,
      displayName,
    }

get:
  headers:
  * Authorization: Bearer <access_token>
"""
class Info(Resource):
  def get(self):

    try: # Check if header exist
      bearer_token = request.headers['Authorization']
    except KeyError:
      return {'message': 'INVALID_HEADER'}, 400 # bad request

    if(bearer_token.startswith('Bearer ')):
      bearer_token = bearer_token.replace('Bearer ', '')
    else:
      return {'message': 'INVALID_HEADER'}, 400 # bad request

    response = info(bearer_token)

    return response