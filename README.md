# PYNQ Facial Recognition Implementation
Miami University ECE 387 Spring 2018 Midterm Project

Author: Jacob Iarve

## Getting Started
### Introduction
  For my midterm project, I have interfaced the Xilinx PYNQ-Z1 with a webcam and an HDMI output.
Using PYNQ, it is easy to create overlays that abstract low-level FPGA logic into high 
level languages such as Python 3. Using overlays to program in Python, I installed a Python Facial 
Recognition package that I used to create a Facial Recognition Security System.
  The code for this project works in the following way. It creates I/O Driver objects using OpenCV2
Library to interface a webcam and uses the PYNQ library to interface the HDMI output. After instantiating
each driver, the program will import the facial recognition library and all the images and names for 
each identified individual. Once completed, PYNQ will input every other frame, process the image, and detect
any faces in the frame. In shunt, the program will look to see if the detected face matches any of the 
facial encodings from the identified individuals. If the face matches, the system will print their name
under their face or print "UNKNOWN" if the face is not recognized.
### Demo
[![Click to view on Youtube](https://img.youtube.com/vi/-fjIbl0YfcM/0.jpg)](https://www.youtube.com/watch?v=-fjIbl0YfcM)

Click the image above to be redirected to Youtube and watch a short demo of the project.
### Built With
* OpenCV 2 - Comes installed on PYNQ.
* [Ageitgey Facial Recognition](https://github.com/ageitgey/face_recognition) -Facial Recognition Library Used
* [PYNQ Board](https://github.com/Xilinx/PYNQ) -PYNQ Libraries
### Installation
Interface PYNQ via the Getting Started Guide on [PYNQ.io](http://pynq.readthedocs.io/en/latest/getting_started.html). Make sure to connected via the Ethernet mode. 
Once connected, open up a Terminal in Jupyter notebooks and run the following command:
```
sudo pip install git+https://github.com/ageitgey/face_recognition
```
The installation may take many hours to complete.

Once completed the user can simply upload pictures via juptyer notebooks and redirect them to easily found
file location and paste these into the code with the identified individuals name. [My code](https://github.com/IarveJ/PYNQ_facialRec/blob/master/PYNQ_FacialRecognition.py).
is a simple example that can be used to run this system.

## Project Topics
### Development
To develop this code, I first used the [Webcam Face Detection](https://github.com/Xilinx/PYNQ/blob/v1.4/Pynq-Z1/notebooks/examples/opencv_face_detect_webcam.ipynb) example found in the Juptyer Notebook Files of PYNQ. 
This example allowed me to simply take a picture with openCV face detection, and display the resultant image via HDMI out.
Using this code I implemented a loop that allowed for the camera to work in video. Due to the high amount of output lag, I 
decreased the processing to every other frame. Finally, I used the [Raspberry Pi example](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py) noted in Ageitgey's and integrated
the code to work with the PYNQ board. Overall, most of the code used was an integration of those two examples.
### Added Value
* Added video image processing from simple capture and display image processing in example.
* Integrated Facial Recognition libary to work on PYNQ
* Extensively used Operating Systems to import image files and install Python Library
### References
* [Raspberry Pi example](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py) -Ageitgey's Raspberry Pi example adapted for implemention with PYNQ
* [Webcam Face Detection](https://github.com/Xilinx/PYNQ/blob/v1.4/Pynq-Z1/notebooks/examples/opencv_face_detect_webcam.ipynb) -PYNQ example using OpenCV to interface webcam and HDMI output, and detect faces.



