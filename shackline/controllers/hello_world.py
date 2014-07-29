from flask import jsonify
from flask.ext import restful

class HelloWorld (restful.Resource):
  def get(self):
    return jsonify(hello='world')
