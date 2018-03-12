# PYNQ Facial Recognition Implementation
Miami University ECE 387 Spring 2018 Midterm Project

Author: Jacob Iarve

## Getting Started
### Introduction
For my midterm project, I have interfaced the Xilinx PYNQ-Z1 with a webcam and an HDMI output.
Using PYNQ, it is easy to create overlays that abstract low-level FPGA logic into high 
level languages such as Python 3. Using overlays to program in Python, I installed a Python Facial 
Recognition package that I used to create a Facial Recognition Security System.
### Built With
* OpenCV 2 - Comes installed on PYNQ board.
* [Ageitgey Facial Recognition](https://github.com/ageitgey/face_recognition) -Facial Recognition Library Used
* [PYNQ Board](https://github.com/Xilinx/PYNQ) -PYNQ Board Libraries
### Installation
Interface PYNQ via the Getting Started Guide on [PYNQ.io](http://pynq.readthedocs.io/en/latest/getting_started.html). Make sure to connected via the Ethernet mode. 
Once connected, open up a Terminal in Jupyter notebooks and run the following command:
```
sudo pip install git+https://github.com/ageitgey/face_recognition
```
The installation may take many hours to complete however, once completed the user can simply plug in the drivers and run [my code](https://github.com/IarveJ/PYNQ_facialRec/blob/master/PYNQ_FacialRecognition.py).




