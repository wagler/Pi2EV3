Pi2EV3
======

Code for a Raspberry Pi based robot. Motors driven by Lego EV3.

This library utilizes the Raspberry Pi as an image processing device to track a ball. The EV3 is then told over SSH where to
go and what to do in order to capture the ball.

To setup the EV3 and Raspberry Pi you will need to install the following on the Raspberry Pi:
Opencv-Python, Paramiko-Python
Which are both available on the apt repository system.

To setup the EV3 follow the EV3 Linux Development over at: 
https://github.com/mindboards/ev3dev
