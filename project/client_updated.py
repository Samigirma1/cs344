import cv2
import socket
import struct
import pickle
import keras
import numpy
import tensorflow
import math

print("Geting model files...")
# # load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
print("Loading models...")
loaded_model = keras.models.model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

# # evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# #print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
print("Model compiled")

TCP_IP = '153.106.213.22'
TCP_PORT = 9502
server_address = (TCP_IP, TCP_PORT)
i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
data = b''
payload_size = struct.calcsize("I")

def getframe(data):
    while len(data) < payload_size:
        data += sock.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("I", packed_msg_size)[0]
    while len(data) < msg_size:
        data += sock.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    if frame_data == b'':
        return -1, data, None

    return 0, data, pickle.loads(frame_data)

# send feed
def sendLabel(socket_, prediction):
    emotions = ["neutral", "smiling", "sad", "surprise-shock", "angry", "disgusted", "fearful"]

    response = emotions[prediction.index(max(prediction))]
    prediction.pop(prediction.index(max(prediction)))
    if max(prediction) > 0.5:
        response = response + " / " + emotions[prediction.index(max(prediction))]

    socket_.send(bytearray(response, "utf-8"))


while True:
    flag, data, frame = getframe(data)
    if (flag == -1):
        break
    frame = cv2.resize(frame, (256, 256), interpolation=cv2.INTER_AREA)
    predictions = loaded_model.predict(numpy.reshape(frame, (1, 256, 256, 3)))
    print(predictions)
    sendLabel(sock, predictions[0].tolist())

sock.close()
