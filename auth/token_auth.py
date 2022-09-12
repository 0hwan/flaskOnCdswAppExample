from flask import request, Response, jsonify, make_response
from functools import wraps

def api_authorization(func):
    @wraps(func)
    def validate_bearer_token(*args, **kwargs):
        result = func(*args, **kwargs)
        token = request.headers.get("Authorization")
        if token is None:
            return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
            # return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
        
        return result
    return validate_bearer_token

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        print("=========> token [%s]" % token)
        if token is None:
            return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        # auth = request.authorization
        
        # if not auth or not auth.username or not auth.password:
        #     return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        return f(*args, **kwargs)
    return wrapper