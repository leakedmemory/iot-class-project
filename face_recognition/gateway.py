import cv2
import urllib.request
import numpy as np
# from custom_objects import *
import paho.mqtt.client as paho
import time
import json
f_cas = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
URL = 'http://192.168.1.3/640x480.jpg'
MODEL_PATH = 'model.h5'
BROKER="192.168.1.9"
PORT=1833

# cv2.namedWindow("Live Transmission", cv2.WINDOW_AUTOSIZE)

index = 0
allow = True

# model = tf.keras.models.load_model(MODEL_PATH, {"L1Dist": L1Dist})

try:
    client = paho.Client("ESP-CAM")
    client.username_pw_set("ifpb", "ifpb")
    client.connect(BROKER, PORT)
    client.loop_start()
except:
    exit()
count = 0
while True:
    img_resp=urllib.request.urlopen(URL)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgnp,-1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face=f_cas.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    if len(face) == 1:
        count += 1
        x,y,w,h = face[0]
        if x and y:
            index += 1
          
        # faceImg = img[y:y+250, x:x+250]
        # faceImg = cv2.resize(img, dsize=(105, 105))

        # validationImage = cv2.imread('lohan.jpg')
        # validationImage = cv2.resize(validationImage, dsize=(105, 105))

        # cv2.imwrite(f"face-{index}-faceImg.jpg", faceImg)
        # cv2.imwrite(f"face-{index}-validation.jpg", validationImage)

        # faceImg = faceImg/255.0
        # validationImage = validationImage/255.0

        # faceImg = faceImg.reshape(1, 105, 105, 3)
        # validationImage = validationImage.reshape(1, 105, 105, 3)

        # predictions = model.predict([faceImg, validationImage])
        # if predictions[0][0] > 0.5:
        #     print("EH A PESSOA")
        # else:
        #     print("EH IMPOSTOR")
        if count == 5:
            print("permitido")
            client.publish("status",  json.dumps({"allow": True, "name": "Lucas"}))
            count = 0
        # time.sleep(2000)



    # cv2.imshow("live transmission",img)
    # key=cv2.waitKey(5)
    # if key==ord('q'):
        # break
 
# cv2.destroyAllWindows()