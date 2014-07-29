from flask import send_file, jsonify
from flask.ext import restful
from PIL import Image
import requests, urllib, time

class GetImage (restful.Resource):

  IMAGE_CHK = 'http://www.shakeshack.com/camtest.php'
  IMAGE_SRC = 'http://www.shakeshack.com/camera.jpg'
  IMAGE_TRG = '/tmp/frame'
  DELAY = 10

  def get(self):
    self.getFrame()
    return jsonify(status="done")

  def checkFrame(self):
    req = requests.get(self.IMAGE_CHK)
    if(req.content == 'GOOD') : return True
    return False

  def getFrame(self):
    i = 0
    for i in range(0, 12):
      while self.checkFrame() is False:
        pass
      urllib.urlretrieve(self.IMAGE_SRC, self.IMAGE_TRG + `i` + '.jpg')
      time.sleep(self.DELAY)
