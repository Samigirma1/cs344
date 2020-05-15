from __future__ import print_function
import cv2 as cv
from PIL import Image
import argparse

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    print(faces)

    i = 0
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        cv.imwrite("result" + str(i) + ".jpeg", faceROI)
        i+=1

face_cascade_name = "./openCVcascades/face_detector.xml"#args.face_cascade
face_cascade = cv.CascadeClassifier()

#-- 1. Load the cascades
if not face_cascade.load(face_cascade_name):
    print('--(!)Error loading face cascade')
    exit(0)

im = cv.imread("./hard.jpg")
detectAndDisplay(im)
