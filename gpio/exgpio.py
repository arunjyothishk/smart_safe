"""
 ============================================================================
 Name        : jeis_ss@jotix.py
 Author      : ARUN JYOTHISH  K
 Version     :1.0
 Copyright   : Your copyright notice
 Description : 'Smart Safe', 2 step authentication locker system with iot
 ============================================================================
 """
#raspberry gpio importing for using it from python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

matrO=[11,13,15]
matrI=[31,33,35,37]
ledO=[19,22,32,36,38,40]

op=ledO+matrO
for i in op:
     GPIO.setup(i,GPIO.OUT)
for i in matrI:
     GPIO.setup(i,GPIO.IN)

def led(k):
     n=ledO[k]
     GPIO.output(n,True)
     time.sleep(.1)
     GPIO.output(n,False)
     time.sleep(.8)

def button(rawO,coloumnI):
     led(rawO)
     led(coloumnI)

def push():
     for i in matrO:
          GPIO.output(i,True)
          for j in matrI:
               if GPIO.input(j):
                    button(i,j)
          GPIO.output(i,False)
while True:
     led(2)
     led(3)
     led(0)
     led(0)
