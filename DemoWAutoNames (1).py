
# coding: utf-8

# In[ ]:

##########################################################
###### CREATE Video Input/Output Drivers #################
##########################################################

print("Program Started\nInstantiating Drivers")

from pynq import Overlay
import numpy as np
import cv2
from pynq.drivers.video import HDMI


Overlay("base.bit").download()

# monitor configuration: 640*480 @ 60Hz
hdmi_out = HDMI('out', video_mode=HDMI.VMODE_640x480)
hdmi_out.start()


# monitor (output) frame buffer size
frame_out_w = 1920
frame_out_h = 1080
# camera (input) configuration
frame_in_w = 640
frame_in_h = 480

# initialize camera from OpenCV
from pynq.drivers.video import Frame

webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_in_w);
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_in_h);

print("Capture device is open: " + str(webcam.isOpened()))

##########################################################
########### FACIAL RECONGITION IMPORT ####################
##########################################################

print("Import Started... ")

import face_recognition
import glob
import os
import sys

##########################################################
######### Folder with People/Pictures I/O  ###############
##########################################################

pathArray=glob.glob("/home/xilinx/pynq/knownPeople/*.jpg")
known_face_names = []
known_face_encodings = []

for i in pathArray:
    name = i[30:len(i)]
    nameLength = len(name)
    name = name.split(".")[0]
    known_face_names.append(name)
    
    image = face_recognition.load_image_file(i)
    known_face_encodings.append(face_recognition.face_encodings(image)[0])
    
    
print("Found " + str(len(pathArray)) + " people")    
       
##########################################################
###### Data Variables for Known People  ##################
##########################################################    

frames = [] 
frame_count = 0
face_locations = []
face_encodings = []
face_names = []

print("Face Import Complete")


##########################################################
###### RUN FACIAL RECONGITION SYSTEM #####################
##########################################################

print("Executing")

from pynq.board import Button
import asyncio 

stopButton = Button(0)

process_this_frame = True

ret, frame = webcam.read()
x = 0

while webcam.isOpened():
    ret, frame = webcam.read()
    frame_1080p = np.zeros((720,1920,3)).astype(np.uint8)       
    
    #Resize Frame BGR
    inputBGR = cv2.resize(frame, (0,0),fx=0.25, fy=0.25)
    #Convert to facial_recogntion encoding BGR -> RGB 
    rgb_small_frame = inputBGR[:,:,::-1]
    
    frame_count += 1
    frames.append(rgb_small_frame)

    if stopButton.read():
       
        break
    
    
    
    # Only process every other frame of video to save time
    if x%4 == 0 : 
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

            
            
    # Display the results
    if x%4 == 0:
        for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

        # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left, bottom - 10), font, 1.0, (255, 255, 255), 1)

    #outputBGR = rgb_small_frame[...,::-1]
    
        frame_1080p = np.zeros((1080,1920,3)).astype(np.uint8)       
        frame_1080p[0:480,0:640,:] = frame[0:480,0:640,:]
        hdmi_out.frame_raw(bytearray(frame_1080p.astype(np.int8)))
    
    
    
    x += 1
    
    
##########################################################
###### Once System is stopped Release Drivers ############
##########################################################


webcam.release()
hdmi_out.stop()
del hdmi_out
print("Program Stopped")


# In[ ]:




# In[2]:




# In[ ]:



