from flask import Flask
from flask import request, Response
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/test/hello', methods=['GET'])
def hellof():
	return "hello"

if __name__ == '__main__':
	app.run(host='0.0.0.0')
