from flask import request, jsonify, abort
from flask_restful import Resource

from firebase import refreshToken

"""
Refresh token endpoint for updating access (and refresh) token
/api/auth/refresh

returns:
  * 400, INVALID_BODY - On refreshToken property in body not existing
  * 503, SERVICE_OFFLINE - On firebase not being init
  * 400, INVALID_REFRESH_TOKEN - On refresh token not being valid
  * 201, - On successful refresh:
    {
      accessToken,
      refreshToken,
    }

post:
  body (json):
  {
    refreshToken,
  }
"""
class Refresh(Resource):
  def post(self):
    request_data = request.get_json()

    try: # Check if properties exist
      token = request_data['refreshToken']
    except KeyError:
      return {'message': 'INVALID_BODY'}, 400 # bad request

    response = refreshToken(token)

    return response