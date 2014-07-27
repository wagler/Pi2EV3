Pi2EV3
======

Code for a Raspberry Pi based robot. Motors driven by Lego EV3.

This library utilizes the Raspberry Pi as an image processing device to track a ball. The EV3 is then told over SSH where to
go and what to do in order to capture the ball. The Raspberry Pi will then guide the robot back to home base.

To setup the EV3 and Raspberry Pi you will need to put the Debian distro for EV3 on a micro SD card. You will also need to download "python-opencv" on the Raspberry Pi. This can be done at the terminal via: "sudo apt-get upgrade", then "sudo apt-get install python-opencv". Finally, you need to put the server.py file on the EV3, and imgproc.py on the Raspberry Pi.

To setup the EV3 and for general API info, follow the EV3 Linux Development over at: 
https://github.com/mindboards/ev3dev
