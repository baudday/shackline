from flask import send_file, jsonify
from flask.ext import restful
import os

class GetCount (restful.Resource):

  def get(self):
    dir = os.path.realpath('/home/willem/projects/shackline/')
    logpath = os.path.join(dir, 'line_status.txt')
    fileHandle = open(logpath, 'r')
    lines = fileHandle.readlines()
    fileHandle.close()
    current = lines[-1]
    arr = current.split(',')
    date = arr[0].rstrip()
    count = float(arr[2].rstrip())

    if(count < 20.0):
      length = "short"
    elif(count < 40.0):
      length = "medium"
    else:
      length = "long"

    return jsonify(datetime=date, count=count, length=length)
