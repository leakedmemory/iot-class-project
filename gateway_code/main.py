import json
import datetime
import base64
import cv2
import urllib.request
import numpy as np
import paho.mqtt.client as paho
 
f_cas = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
URL = "http://192.168.1.7/640x480.jpg"
BROKER = "localhost"
PORT = 1833
 
index = 0
allow = True
last_input_time = 0
time_in_seconds_from_last_input = 11
 
try:
    client = paho.Client("ESP-CAM")
    client.username_pw_set("ifpb",  "ifpb")
    client.connect(BROKER, PORT)
    client.loop_start()
except:
    exit()
 
print("Iniciando reconhecimento")
while True:
    try:
        img_resp = urllib.request.urlopen(URL)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = f_cas.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(face) == 1 and time_in_seconds_from_last_input > 10:
            print("Face detectada")
            x, y, w, h = face[0]
            if x and y:
                index += 1
 
            im_bytes = imgnp.tobytes()
            im_b64 = base64.b64encode(im_bytes)
            im_b64_str = im_b64.decode('utf-8')
            print("Acesso permitido.")
            client.publish("status", json.dumps({"allow": True, "name": "Lucas"}))
            data = {"image": im_b64_str}
            data = json.dumps(data)
            data = str(data)
            data = data.encode('utf-8')
            try:
                req = urllib.request.Request('http://192.168.1.10:7071/api/logs', method="POST", data=data)
                urllib.request.urlopen(req)
            except Exception as e:
                print("Erro ao tentar salvar imagem do visitante")
                print(e)
            last_input_time = datetime.datetime.now()
            time_in_seconds_from_last_input = 0
        elif time_in_seconds_from_last_input <= 10:
            current_time = datetime.datetime.now()
            time_in_seconds_from_last_input = (current_time - last_input_time).total_seconds()
    except Exception as e:
        print("Error ao tentar capturar imagem da ESPCAM")
        print(e)
