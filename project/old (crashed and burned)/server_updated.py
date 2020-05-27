import cv2
import pickle
import socket
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 9502
video_file = 'facesVid.webm'

# Receive facial expression labels from the server
def receiveLabels(mySocket):
    data = mySocket.recv(1024)
    print(str(data))
    return str(data)

# detects the faces in a frame
def detectAndDisplay(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    face_list = []
    i = 0
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        face_list.append(frame[y:y+h, x:x+w])

    return frame, face_list, faces

face_cascade_name = "./face_detector.xml"#args.face_cascade
face_cascade = cv2.CascadeClassifier()

#-- 1. Load the cascades
if not face_cascade.load(face_cascade_name):
    print('--(!)Error loading face cascade')
    exit(0)

print("Starting server...\n")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # establishing a tcp connection
sock.bind((TCP_IP, TCP_PORT))
sock.listen(5)

while True:
    (client_socket, client_address) = sock.accept()  # wait for server
    print
    'connection established with ' + str(client_address)
    cap = cv2.VideoCapture(video_file)
    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    # send frames
    while True:
        flag, frame = cap.read()
        labels = []
        if flag:
            frame_labelled, face_list, bounds = detectAndDisplay(frame)

            for i in range(len(face_list)):
                a_face = face_list[i]
                a_face = pickle.dumps(a_face)
                size = len(a_face)
                p = struct.pack('I', size)
                a_face = p + a_face
                client_socket.sendall(a_face)

                label = receiveLabels(client_socket)

                frame = cv2.rectangle(
                    frame,
                    (bounds[i][0], bounds[i][1]),
                    (bounds[i][0] + bounds[i][2], bounds[i][1] + bounds[i][3]),
                    (0, 0, 0),
                    1
                )
                frame = cv2.putText(frame, label, (bounds[i][0], bounds[i][1] + bounds[i][3] + 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame - 1)

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            size = 10
            p = struct.pack("I", size)
            client_socket.send(p)
            client_socket.send('')
            break

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)