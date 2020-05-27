import json
import sys
from threading import Thread, Event, Lock
from queue import Queue
import time
import struct
import pickle
from tensorflow import keras
import numpy
import tensorflow as tf
import paho.mqtt.client as mqtt
import cv2 as cv

QOS = 0
BROKER = 'test.mosquitto.org'
PORT = 1883

#thread class to process data
class myThread (Thread):
   def __init__(self, threadID, name, client):
      Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.client =client
    
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.client, model)
      print ("Exiting " + self.name)

#call back for mqtt client
def on_message(client, data, msg):
    if msg.topic == "aiproj/facrecog/image":
        if msg:
            print("message")
            print("item")
            workQueue.put(msg.payload)
            print("released lock")
            print(len(workQueue))

# call back for mqtt client
def on_connect(client, userdata, rc, *extra_params):
   print('Connected with result code='+str(rc))
   client.subscribe("aiproj/facrecog/image", qos=QOS)

#closes client and terminates threads
def kill_command(threads, client):
    print("closing")
    client.close()
    exitFlag.set()
    for t in self.threads:
        t.join()

# sends data to client
def send_response(client, message):
    (result, num) = client.publish('aiproj/facrecog/response', message, qos=QOS)
    print("sent response:", message)
    if result != 0:
        print('PUBLISH returned error:', result)

#uses model to get prediction
def predict(data, model):
    frame = cv.resize(data, (256, 256), interpolation=cv.INTER_AREA)
    with session.graph.as_default():
        keras.backend.set_session(session)
        predictions = model.predict(numpy.reshape(frame, (1, 256, 256, 3)))
        print(predictions)
        return predictions[0].tolist()

#converts the prediction to a string
def getLabel(prediction):
    emotions = ["neutral", "smiling", "sad", "surprise-shock", "angry", "disgusted", "fearful"]
    response = emotions[prediction.index(max(prediction))]
    prediction.pop(prediction.index(max(prediction)))
    if max(prediction) > .5:
        response = response + "/" + emotions[prediction.index(max(prediction))]
    return response

 #work function for threads
def process_data(threadName, client, model):
    while True:
        data = workQueue.get()
        if data:
            print (threadName, "processing an image")
            item = pickle.loads(data)
            message = getLabel(predict(item, model))
            print(threadName, "processed", message)
            #send precition
            sendLock.acquire()
            send_response(client, message)
            sendLock.release()
        else:
            print("...")
        if exitFlag.is_set():
            break
        time.sleep(.25)
#
def init(thread_nums):
    print("*****")
    print("Initializing connection...")
    print("*****")
    client = mqtt.Client()
    threads = []
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    for threadID in range(thread_nums):
        threads.append(myThread(threadID, "Thread"+str(threadID), client))
    for t in threads:
        t.start()
    return threads,client



def load_model():
    print("Geting model files...")
    # # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    print("*****")
    print("Loading models...")
    print("*****")
    session = tf.Session(graph=tf.Graph())
    with session.graph.as_default():
        keras.backend.set_session(session)
        loaded_model = keras.models.model_from_json(loaded_model_json)
        loaded_model.load_weights("model.h5")
        return loaded_model, session
    print("*****")
    print("Loaded model from disk")
    print("*****")
    # # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #graph = tf.get_default_graph()
    print("*****")
    print("Model compiled")
    print("*****")
    

global model
global session
global sendLock
global workQueue
model, session =load_model()
exitFlag = Event()
sendLock = Lock()
connected = Event()
workQueue = Queue(30)
threads,client = init(3)
try:
    client.loop_start()
except KeyboardInterrupt:
    kill_command(threads, client)




