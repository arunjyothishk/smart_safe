
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
matrO=[17,27,22]
matrI=[6,13,19,26]
ledO=[10,25,12,16,20,21]
GPIO.setwarnings(False)

op=ledO+matrO
for i in op:
	GPIO.setup(i,GPIO.OUT)
for i in matrI:
	GPIO.setup(i,GPIO.IN)

list=[]
but=["NONE"]
#MATRIX BUTTONS FN
button=[[1,2,3,'$'],[4,5,6,0],[7,8,9,'%']]
def push():

	for i in matrO:
		GPIO.output(i,False)
		for j in matrI:
			if not GPIO.input(j):
				list.append(i)
				rw=matrO.index(i)
				list.append(j)
				cl=matrI.index(j)
				but.insert(0,button[rw][cl])

		list.append("  ")
		GPIO.output(i,True)
#	print (list)
#MATRIX BUTTONS FN END
push()
print(list)
print(but[0])
#FINISHED DEF LED
