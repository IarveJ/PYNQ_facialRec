# PYNQ Facial Recognition Implementation
Miami University ECE 387 Spring 2018 Final Project

Author: Jacob Iarve

## Getting Started
### Introduction
  For my Final project, I expanded upon interface created between the Xilinx PYNQ-Z1 with a webcam and
an HDMI output for the midterm. Using PYNQ, it is easy to create overlays that abstract low-level FPGA 
logic into high level languages such as Python 3. Using overlays to program in Python, I installed a Python 
Facial Recognition package that I used to create a Facial Recognition Security System. The next step in my 
project was introducing interrupts to stop the processor, and have it make decisions so that this system could 
interact with the user without sacraficing CPU. This is where the project got more complicated. On the PYNQ 
disc image used to boot and operate the PYNQ board, was old programs from an earlier release that did not 
contain the interrupt objects in its library. Thus, to accomplish this I wrote a new image onto a seperate SD card
to boot the system using the new PYNQ image from February 2018. However, using the new image which uses Python 3.3.0,
the system could no longer download Face Recognition due to inheret issues installing facial recognition to the new 
Python update. 

  Having the serious problem of not being able to intergrate the programs to run both facial recognition and interrupts, 
I decided to create a network using two PYNQ boards. One pynq board, using the new image will be a user interface built upon
interrupt framework in the AsyncIO class made from Python. This system will take a webcam picture after a user pushes an 
interrupt. This is caused by the interrupt literally interrupting the ARM processor and executing a function that takes the 
picture and saves it via an inputted name online, as that board acts as server. 
  Once this picture is on the internet, the second PYNQ board with the old disk image and capable of running the facial 
recogntion library is used. This system downloads the picture to a local directory and then executes the facial recognition
system created for the midterm assessment. 
 
### Faical Recognition System
 The code for this project works in the following way. It creates I/O Driver objects using OpenCV2
Library to interface a webcam and uses the PYNQ library to interface the HDMI output. After instantiating
each driver, the program will import the facial recognition library and all the images and names for 
each identified individual. Once completed, PYNQ will input every other frame, process the image, and detect
any faces in the frame. In shunt, the program will look to see if the detected face matches any of the 
facial encodings from the identified individuals. If the face matches, the system will print their name
under their face or print "UNKNOWN" if the face is not recognized.

### Interrupt Enabled System
  The interrupt system uses the python native AsyncIO class to create interrupts to stop the processor.
By defining coroutines, the user can tell the system which interrupts to use and what should happpen 
when one is flagged. Using coroutines you essentially create an event loop and state how long you would 
like it to go and what tasks can happen along the event loop. An interrupt essentially tells the interrupt
to switch states while stopping the processors function to handle the next executable. In my code, I have
abstracted the coroutines to functions called when any interrupt (button or switch) is sent. These classes,
now make it easier to code on top of the AsyncIO event loop. [Click here to view this page.](https://github.com/IarveJ/InterruptsPYNQ)

### System Architecture
  My system has two major drivers that need to be included for the code to execute. The first is a webcam,
  I used the Logitech C270, however any webcam that can be interfaced by OpenCV will work. This webcam is 
  interfaced via USB connection. The second driver is the HDMI output. I have included a HDMI to VGA adapter
  when I ran the system so that it would output to our lab's monitors. Using an adapter does create 
  issues in the execution and these bugs are discussed in the known issues section below. Finally, these drivers
  are interfaced directly to the PYNQ board itself and the machine will run if disconnected to jupyter notebooks. 
### Demo
[![Click to view on Youtube](https://img.youtube.com/vi/-fjIbl0YfcM/0.jpg)](https://www.youtube.com/watch?v=-fjIbl0YfcM)

Click the image above to be redirected to Youtube and watch a short demo of the project.
### Built With
* AsyncIO
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
file location and paste these into the code with the identified individuals name.
[My code](https://github.com/IarveJ/PYNQ_facialRec/blob/master/PYNQ_FacialRecognition.py) is a simple example that can be used to run this system.

# Project Topics
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
### Known Issues
* Output Lag
* Color Distortion
* Output Frame
 
 The first of the known issues is the output lag. From manually timing, the program will input, then process an image for roughly 3 
seconds before outputting it via HDMI. To reduce this output lag, I have the program only processing every other frame making therefore at
30Hz, however the bug persists and does not seem affected by the reduction in processing. Further reduction of processing would put it 
close to, or under the optimal 25Hz which is smooth motion to the human eye. 
 
 The second bug is sometimes the program will output Color Distorted images on to the lab's VGA monitors. This bug does not occur at home 
when directly plugging the system into a TV's HDMI input, but rather appears occassionally (not every time) onto VGA monitors when using a 
passive HDMI to VGA adapter. This bug is similar to the third bug, the Output Frame issue, where the system will shift all the array 
values and move the image to the right when outputting to via the VIA adapter.
### References
* [Raspberry Pi example](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py) -Ageitgey's Raspberry Pi example adapted for implemention with PYNQ
* [Webcam Face Detection](https://github.com/Xilinx/PYNQ/blob/v1.4/Pynq-Z1/notebooks/examples/opencv_face_detect_webcam.ipynb) -PYNQ example using OpenCV to interface webcam and HDMI output, and detect faces.



