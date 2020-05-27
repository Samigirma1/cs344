from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ListProperty  
from kivy.graphics.texture import Texture
import time
from threading import Thread, Event, Lock
import cv2
from queue import Queue
import pickle
import struct
import paho.mqtt.client as mqtt
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle  
from kivy.core.window import Window


Builder.load_string('''
<FormattedLabel>:  
    text: root.text
    fontSize: 70 
    color: (0, 0.2, .4, 1)  
    size_hint: 1, 0.04  
    background_color: 0,0,0,1
    '''
    )
'''
<Divider>:  
color: (1, 0.2, .4, .2)  
background_color: 1,0,0,0   
'''
# class for managing the label display
class FormattedLabel(Label):
    background_color = ListProperty()  

    def __init__(self):  
        super(FormattedLabel, self).__init__()  
        Clock.schedule_once(lambda dt: self.initialize_widget(), 0.002)

    def initialize_widget(self):
        self.canvas.before.add(Color(self.background_color))  
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))  
        self.text_size = self.size  
        self.text ="Searching for face..."
        self.halign = 'center'  
        self.valign = 'top'  
        self.bold = True  
    
    def update(self, text):
        self.text = text

class Divider(Widget):
    def __init__(self, **kwargs):
        super(Divider, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 0, 0, 1)  # set the colour to red
            self.rect = Rectangle(pos=self.center,
                                  size=(Window.size[0],
                                        self.height/8.))
    def update(self, color):
        with self.canvas:
            Color(color)  # set the colour to red
            self.rect = Rectangle(pos=self.top,
                                  size=(Window.size[0],
                                        self.height/8.))
              
#class for displaying camerafeed
class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps) # updates in response to framerate

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture
            

#main up
class RecogApp(App):

    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        self.total = GridLayout(rows=2)
        self.label = FormattedLabel()
       # self.divider = Divider()
        self.total.add_widget(self.my_camera)
        #self.total.add_widget(self.divider)
        self.total.add_widget(self.label)
        return self.total

    def on_stop(self):
        print("*** closing...")
        exit.set()
        cam.join()


    def on_start(self):
        QOS = 0
        BROKER = 'test.mosquitto.org'
        PORT = 1883

        def on_connect(client, userdata, rc, *extra_params):
            print('Connected with result code='+str(rc))
            client.subscribe("aiproj/facrecog/response", qos=QOS)

        def send_image(face, frame):
            (result, num) = client.publish('aiproj/facrecog/image', face, qos=QOS)
            print(result, num)
            if result != 0:
                print('PUBLISH returned error:', result)

        def on_message(client, data, msg):
            if msg.topic == "aiproj/facrecog/response":
                if msg:
                    print("recieved message: ", str(msg.payload.decode()))
                    self.label.update("Emotion: "+ str(msg.payload.decode()))

        def detectAndDisplay(frame):
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.equalizeHist(frame_gray)
            faces = face_cascade.detectMultiScale(frame_gray)
            face_list = []
            i = 0
            for (x,y,w,h) in faces:
                center = (x + w//2, y + h//2)
                face_list.append(frame[y:y+h, x:x+w])
            return frame, face_list, faces

        def poll():
            while True:
                flag, frame = self.capture.read()
                labels = []
                if flag:
                    frame_labelled, face_list, bounds = detectAndDisplay(frame)
                    if len(face_list) == 0:
                        self.label.update("Searching for face...")
                    for i in range(len(face_list)):
                        a_face = face_list[i]
                        a_face = pickle.dumps(a_face)
                        send_image(a_face, frame)
                if exit.is_set():
                    break
            #time.sleep(.5)
            
        #get the dimintions of the image
        pos_frame = self.capture.get(cv2.CAP_PROP_POS_FRAMES) 
        face_cascade_name = 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier()
        face_cascade.load(face_cascade_name)
        
        '''
        server = Thread(target=start_server)
        start the thread
        server.daemon = True
        server.start()
        '''
        global client 
        global exit
        global cam
        exit = Event()
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER, PORT, 60)
        cam = Thread(target=poll)
        client.loop_start()
        cam.start()      

        
if __name__ == '__main__':
    app = RecogApp()
    app.run()
