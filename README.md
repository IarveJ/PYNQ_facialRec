# PYNQ_facialRec
Embedded facial recognition system involving PYNQ board, Webcam, and HDMI output. 


This system was developed for educational purposes. 
For Miami University Spring 2018 ECE 387: Embedded Systems Design course.

Hardware setup instructions:

Attach MicroUSB to computer and Ethernet to computer and PYNQ board.
Place preloaded SIMcard with the PYNQ.io data on it into the board.
Set JP4 Boot Jumper to SD.
Set JP3 Boot Jumper to USB.

Board should false blue and green once turned on successfully.

Plug in Webcam to USB slot.
Plug in HDMI out to selected output display.


Software Set up Instructions:
Install Jupyter Notebooks.

Open up Terminal (MAC)
run Jupyter Notebook -once webpage pops up.

Open up Settings:
Set Ethernet Connection to a static IP adress.

Open up Chrome (preferred browser)
Go to url:   192.168.2.99:9090

Run selected program sequentially via Python 3 Notebook.
