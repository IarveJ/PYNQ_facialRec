
# coding: utf-8

# In[1]:


import asyncio
from psutil import cpu_percent
from pynq.overlays.base import BaseOverlay
from pynq.lib import Switch
import numpy as np
import cv2
import glob 
import os
import sys
from pynq import PL
from PIL import Image as PIL_Image
from pynq.lib.video import *
import time


# monitor (output) frame buffer size
frame_out_w = 1920
frame_out_h = 1080
# camera (input) configuration
frame_in_w = 640
frame_in_h = 480

base = BaseOverlay("base.bit")

#videoIn = cv2.VideoCapture(0)
#videoIn.set(cv2.CAP_PROP_FRAME_WIDTH, frame_in_w);
#videoIn.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_in_h);

#print("Capture device is open: " + str(videoIn.isOpened()))

Mode = VideoMode(640,480,24)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(Mode,PIXEL_BGR)
hdmi_out.start()

startTime = 0
endTime = 0


slideShow = False
cameraOn = False

print('starting run')


# Create objects for both switches.
switches = [Switch(i) for i in range(2)]
time_interval = 60 # time in seconds the program will run
known_face_names = [] 

pathArray=glob.glob("/home/xilinx/jupyter_notebooks/knownPeople/*.jpg")
for i in pathArray:
    name = i[43:len(i)]  #concastinate name from string
    nameLength = len(name)
    name = name.split(".")[0]
    known_face_names.append(name)


def switch1HIGH():
    #print("switch 1 HIGH")
    start = time.time()
    turnOnCamera()
def switch1LOW():
    #print("switch 1 LOW")
    turnOffCamera()
def switch0HIGH():
    #print("switch 1 HIGH")
    startSlide()
def switch0LOW():
    #print("switch 0 LOW")
    stopSlide()
           
def button1():
    print("button 1 pressed")
def button2():
    print("button 2 pressed")
def button3():
    #print("button 3 pressed")
    personInput()
def button0():
    #print("button 0 pressed")
    processPersons()   
    
tokenDict = {0:button0, 1:button1, 2:button2, 3:button3}
    
# Coroutine that waits for a switch to change state.
async def show_switch(sw):
    while True:
        # Wait for the switch to change and then print its state.
        await sw.interrupt.wait()  # Wait for the interrupt to happen.
        #print('Switch[{num}] = {val}'.format(num=sw.index, val=sw.read()))
        if sw.index == 1 and sw.read() == 1:
            switch1HIGH()
        if sw.index == 1 and sw.read() == 0:
            switch1LOW()
        if sw.index == 0 and sw.read() == 1:
            switch0HIGH()
        if sw.index == 0 and sw.read() == 0:
            switch0LOW()
        if Switch._mmio.read(0x120) & 0x1:
            Switch._mmio.write(0x120, 0x00000001)
            
async def buttonPressed(num):
    while True:
        await base.buttons[num].wait_for_value_async(1)
        while base.buttons[num].read():
            functionToCall = tokenDict[num]
            functionToCall()
            base.leds[num].toggle()
            await asyncio.sleep(0.1)
        base.leds[num].off()
        
async def turnOnCameraTwo():
    while True:
        await cameraOn.wait_for_value_async(1)
        ret, frame_vga = videoIn.read()
        # Display webcam image via HDMI Out
        if (ret):      
            outframe = hdmi_out.newframe()
            outframe[0:480,0:640,:] = frame_vga[0:480,0:640,:]
            hdmi_out.writeframe(outframe)
            await asyncio.sleep(0.1)
            turnOnCamera()
        else:
            raise RuntimeError("Failed to read from camera.")
        
        
def turnOnCamera():
    
    hdmi_out.start()
    ret, frame_vga = videoIn.read()
    # Display webcam image via HDMI Out
    while (ret):    
        #framesProcessed += 1
        outframe = hdmi_out.newframe()
        outframe[0:480,0:640,:] = frame_vga[0:480,0:640,:]
        hdmi_out.writeframe(outframe)
        #time.sleep(0.5)
    else:
        print('Error Reading From Camera')
        #raise RuntimeError("Failed to read from camera.")
        
def turnOffCamera():
    endTime = time.time()
    #print("Frames per second:  " + str(framesProcessed / (end - start)))
    print('Time[{start},{end}]'.format(start = startTime, end = endTime))
    
   
    
def personInput():
    knownPersonName = input("Enter your name: ")
    known_face_names.append(knownPersonName) #Add Person to List
    orig_img_path = '/home/xilinx/jupyter_notebooks/knownPeople/{name}.jpg'.format(name = knownPersonName)
    get_ipython().system('fswebcam  --no-banner --save {orig_img_path} -d /dev/video0 2> /dev/null')
    print('File saved to /n {path}'.format(path = orig_img_path) )
    

def processPersons():
    print(known_face_names)
    
def startSlide():
    slideshow = True
    
    
def stopSlide():
    slideshow = False
    
    
    
# Create a task for each switch using the coroutine and place them on the event loop.
tasks = [asyncio.ensure_future(show_switch(sw)) for sw in switches]
tasks = [asyncio.ensure_future(buttonPressed(i)) for i in range(4)]
    
# Create a simple coroutine that just waits for a time interval to expire.
async def just_wait(interval):
    await asyncio.sleep(interval)

# Run the event loop until the time interval expires,
# printing the switch values as they change.

loop = asyncio.get_event_loop()
wait_task = asyncio.ensure_future(just_wait(time_interval))



# Surround the event loop with functions to record CPU utilization.
cpu_percent(percpu=True)  # Initialize the CPU monitoring.
loop.run_until_complete(wait_task)
#except RuntimeError:
    #print("Event loop already Running")
cpu_used = cpu_percent(percpu=True)

# Print the CPU utilization % for the interval.
print('CPU Utilization = {cpu_used}'.format(**locals()))

# Remove all the tasks from the event loop.
for t in tasks:
    t.cancel()
    
#videoIn.release()
hdmi_out.stop()
del hdmi_out


# In[2]:


videoIn.release()
hdmi_out.stop()
del hdmi_out

