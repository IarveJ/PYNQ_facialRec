# This code was developed by Jacob Iarve for academic use at Miami University
# The following code creates I/O drivers and uses Ageitgey's open source
# Facial Recognition Library to detect faces via webcam and output via HDMI
# a video of a target with a box around their face, and their name.

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

print("capture device is open: " + str(webcam.isOpened()))

##########################################################
###### FACIAL RECONGITION IMPORT #########################
##########################################################

print("Import Started... ")

import face_recognition
jake_image = face_recognition.load_image_file("/home/xilinx/pynq/Jake.jpg")
jake_face_encoding = face_recognition.face_encodings(jake_image)[0]

nicky_image = face_recognition.load_image_file("/home/xilinx/pynq/Nicky.jpg")
nicky_face_encoding = face_recognition.face_encodings(nicky_image)[0]


known_face_encodings = [
    jake_face_encoding,
    nicky_face_encoding
]

known_face_names = [
    "Jake",
    "Nicky"
]

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

while True:
    ret, frame = webcam.read()
    frame_1080p = np.zeros((1080,1920,3)).astype(np.uint8)       
    
    #Resize Frame BGR
    inputBGR = cv2.resize(frame, (0,0),fx=0.25, fy=0.25)
    #Convert to facial_recogntion encoding BGR -> RGB 
    rgb_small_frame = inputBGR[:,:,::-1]
    

    if stopButton.read():
        print("Program Stopped")
        break
    
    # Only process every other frame of video to save time
    if process_this_frame:
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

    process_this_frame = not process_this_frame


    # Display the results
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
    
##########################################################
###### Once System is stopped Release Drivers ############
##########################################################


webcam.release()
hdmi_out.stop()
del hdmi_out


# In[ ]:




# In[2]:




# In[ ]:



