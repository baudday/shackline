from PIL import Image
import cv2, math, os, re, requests, time, urllib
import numpy as np

FRAME_COUNT = 12
FRAME_LOC = '/tmp/frame'
FRAME_FORMAT = '.jpg'
FRAME_W = 1280
FRAME_H = 720
IMAGE_CHK = 'http://www.shakeshack.com/camtest.php'
IMAGE_SRC = 'http://www.shakeshack.com/camera.jpg'
IMAGE_TRG = '/tmp/frame'
DELAY = 10

def getFrames():
  i = 0
  for i in range(0, FRAME_COUNT):
    while checkFrame() is False:
      pass
    while True:
      try:
        urllib.urlretrieve(IMAGE_SRC, IMAGE_TRG + `i` + FRAME_FORMAT)
      except:
        continue
      break
    time.sleep(DELAY)

def checkFrame():
  req = requests.get(IMAGE_CHK)
  if(req.content == 'GOOD') : return True
  return False

# Get 10 frames
getFrames()

# Subtract background
i = 0
fgbg = cv2.createBackgroundSubtractorMOG2(12, 40, False)
for i in range(0, FRAME_COUNT):
  frame = cv2.bilateralFilter(cv2.imread(FRAME_LOC + `i` + FRAME_FORMAT), 9, 100, 100)
  fgmask = fgbg.apply(frame)

  # Cropped image with people isolated
  final = fgmask[0:FRAME_H, 150:FRAME_W]
  cv2.circle(final, (1130,720), 640, (0,0,255), -1)

# Save the image for reference
cv2.imwrite('/tmp/' + time.strftime("%c") + FRAME_FORMAT, final)


# Get % diff and save in ../line_status.txt with timestamp
hist = cv2.calcHist([final],[0],None,[256],[0,256])
percent = (hist[255][0]/813600)*100

# people = math.floor((percent**2)-(0.535898*percent)+(0.0717968))
# people = math.floor(1.20926*math.exp(0.325364*percent))
# people = math.floor(-0.426698*(percent**2)+11.3195*percent-13.9662)
# people = math.floor(0.5*(percent**2)+0.5*percent)
A = 0.16382
B = 4.26322
C = -14.2098
ZERO = 2.9897

if(percent < ZERO):
  people = 0
else:
  # people = math.floor((0.238213)*(percent**2)-(0.187261*percent)-0.727829)
  people = math.floor(A*(percent**2)+(B*percent)+C)

dir = os.path.realpath('/home/willem/projects/shackline/')
logpath = os.path.join(dir, 'line_status.txt')
with open(logpath, "a") as log:
    log.write(time.strftime("%c") + "," + `percent` + "," + `people` + "\n")
