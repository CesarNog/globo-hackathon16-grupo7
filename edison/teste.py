# -*- coding: utf-8 -*-

from Servo import *
import time

import socket
HOST = '192.168.1.35'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)

# Create a new servo object with a reference name
myServo = Servo("First Servo")

# Attaches the servo to pin 3 in Arduino Expansion board
myServo.attach(3)
angle = myServo.read()


def left(angle):
	for i in range (angle, angle-45, -1):
		myServo.write(i)
		
	
	return(angle-45)
	

def right(angle):
	for i in range (angle, angle+45):
		myServo.write(i)

	return(angle+45)	 
try:
	while True:

		msg, cliente = udp.recvfrom(1024)
	
	
		if (msg == "esquerda"):
			angle = left(angle)
			print "esquerda"
		elif (msg == "direita"):
			angle = rigth(angle)
			print "direita"

            
except KeyboardInterrupt:
       print "Sweep ended."
