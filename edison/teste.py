# -*- coding: utf-8 -*-

from Servo import *
import time

import cv2

webcam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('base.xml')
width = webcam.get(3)

# Create a new servo object with a reference name
myServo = Servo("First Servo")

# Attaches the servo to pin 3 in Arduino Expansion board
myServo.attach(3)
#angle = myServo.read()


def left(angle):
	for i in range (angle, angle-45, -1):
		myServo.write(i)
		
	
	return(angle-45)
	

def right(angle):
	for i in range (angle, angle+45):
		myServo.write(i)

	return(angle+45)	 
try:
	while cv2.waitKey(True) != 27:
		_, img = webcam.read()
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		#cv2.line(img, (int(width/2), 0), (int(width/2), int(webcam.get(4))), (0, 255, 0), 2)
		#cv2.line(img, (int(width/2) - int(width/4), 0), (int(width/2) - int(width/4), int(webcam.get(4))), (0, 0, 255), 2)
		#cv2.line(img, (int(width/2) + int(width/4), 0), (int(width/2) + int(width/4), int(webcam.get(4))), (0, 0, 255), 2)
		for x, y, w, h in faces:
			cx, cy = x+w/2, y+h/2
			#cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
			#cv2.line(img, (cx, cy), (cx, cy), [0, 255, 255], 15)
			
			print myServo.read()
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			if (cx, cy) < (int(width/2) - int(width/4), 0):
        		#	angle = left(angle)
        			print "esquerda"
			elif (cx, cy) > (int(width/2) + int(width/4), 0):
        		#	angle = rigth(angle)
				print "direita"
#   		cv2.imshow('img', img)


            
except KeyboardInterrupt:
       print "Sweep ended."
