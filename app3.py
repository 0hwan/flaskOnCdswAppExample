from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource
from functools import wraps
import jsonify
from auth import token_auth

app = Flask(__name__)
# api = Api(app)

def check_login(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs): 
        print('jfsklajflsajl')
        return func 
    return wrapper 


@app.route('/hello', methods=['GET'])
@token_auth.document_it
def get_hello():
    print("Hello GET")
    return jsonify({'message' : 'new book created'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9999)