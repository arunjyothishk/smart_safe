
import Adafruit_SSD1306
import time
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO
import picamera
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

#mail sending setups
fromaddr = "jeisdevice0@gmail.com"
toaddr = "arunjyothishvikku@gmail.com"
mail = MIMEMultipart()
mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "Attachment"
body = "Please find the attachment"
#what include in contents
#sendmail function
def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    print data
    dat='%s.jpg'%data
    print dat
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "your password")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
#sendmail function

#to capture the image of threat
def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print data
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)
#fn finished picture capture of threat
#initialize camera settings
"""
camera = picamera.PiCamera()
camera.rotation=180
camera.awb_mode= 'auto'
camera.brightness=55
#initialization finished
"""
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

matrO=[17,27,22]
matrI=[10,9,11,5]
fngrI=[18]
ledO=[13,19,26,16,20,21]

op=ledO+matrO+fngrI
ip=matrI+fngrI
for i in op:
	GPIO.setup(i,GPIO.OUT)
	GPIO.output(i,False)
for i in ip:
	GPIO.setup(i,GPIO.IN)

## Tries to initialize the sensor
try:
	f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

	if ( f.verifyPassword() == False ):
		raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
	print('The fingerprint sensor could not be initialized!')
	print('Exception message: ' + str(e))
	exit(1)

GPIO.output(ledO[0],True)

import subprocess

RST = None     # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding+28
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()


#some global variable
l2=30
l22=15
usrname=['jyothish k','Arun k','Ashwin c','Vyshak ms','jishal p','shanid p','Rishad Babu','Sadhique Ali',"unknown..!"]



def stats_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    draw.text((25,0),"JEIS ROBOTICS",font=font,fill=255)
    draw.text((0,14),"Smart Safe",font=font,fill=255)
    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
    draw.text((x,top+8),     str(CPU), font=font, fill=255)
    draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
    draw.text((x, top+25),    str(Disk),  font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def fingerfn_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
   # print("value of top",top)
    draw.text((x, 15),       "S C A N N I N G... " ,  font=font, fill=255)
    draw.text((x+15, l2),     "fingerprint..../", font=font, fill=255)
    draw.text((x, l2+16),   "Tmpl/$."+ str(f.getTemplateCount()),  font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)


def grnt_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
   # print("value of top",top)
    draw.text((x, 15),       "A C C E S S " ,  font=font, fill=255)
    draw.text((x+50, l2),     "G R A N T E D....", font=font, fill=255)
    draw.text((x+50, top+35),   "***",  font=font, fill=255)
    draw.text((x+45, top+40),   "**",  font=font, fill=255)
    GPIO.output(ledO[5],True)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def denied_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
   # print("value of top",top)
    draw.text((x, 15),       "A C C E S S " ,  font=font, fill=255)
    draw.text((x+50, l2),     "D E N I E D....!", font=font, fill=255)
    draw.text((x+50, top+35),   "***",  font=font, fill=255)
    draw.text((x+45, top+40),   "**",  font=font, fill=255)
    GPIO.output(ledO[4],True)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def passed_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, 15),       "P A S S E D .... " ,  font=font, fill=255)
    draw.text((x+25, l2),     "Routing to usr..../", font=font, fill=255)
    GPIO.output(ledO[3],True)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def failed_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, 15),       "F A I L E D .... " ,  font=font, fill=255)
    draw.text((x+15, l2),     "No usr match found.", font=font, fill=255)
    GPIO.output(ledO[2],True)
    disp.image(image)
    disp.display()
    time.sleep(.1)


def usr_disp(k,pos):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    Time=datetime.datetime.now().replace(microsecond=0).time()
    Date=datetime.datetime.now().date()
   # print("value of top",top)
    draw.text((x, 05),       "LOG .... " ,  font=font, fill=255)
    draw.text((x, l22+5),     "usr: "+str(usrname[pos]), font=font, fill=255)
    draw.text((x, 40),     "Date : "+str(Date), font=font, fill=255)
    draw.text((x, 50),     "Time : "+str(Time), font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def iot_disp(k,pos):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, 15),       "U N L O C K E D .... " ,  font=font, fill=255)
    draw.text((x+30, l2),     "via IoT key", font=font, fill=255)
    draw.text((x, top+26),   "_ by usr : "+str(usrname[pos]),  font=font, fill=255)
    GPIO.output(ledO[1],True)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def pin_disp(k,pos):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, 0),       "E N T E R __P I N " ,  font=font, fill=255)
    draw.text((x, l22),     str(usrname[pos])+"@ : ", font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def unlocked_disp(k):
    if k == False:
            return
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, 15),       "U N L O C K E D /... " ,  font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)


def fscanner_disp(k):
	if k == False:
		return
	templates=str(f.getTemplateCount())
	storageof=str(f.getStorageCapacity())
	## Gets some sensor information
	print('Currently used templates: ' + templates +'/'+ storageof )
	## Tries to search the finger and calculate hash
	try:
		print('Waiting for finger...')

		## Wait that finger is read
		while ( f.readImage() == False ):
			pass
		## Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)
           ## Searchs template
		result = f.searchTemplate()

		positionNumber = result[0]
		accuracyScore = result[1]
		print("match found")
		if ( positionNumber == -1 ):
			print('No match found!')
			failed_disp(1)
		else:
			passed_disp(1)
			print('Found template at position #' + str(positionNumber))
			print('The accuracy score is: ' + str(accuracyScore))

		## OPTIONAL stuff
	except Exception as e:
		print('Operation failed!')
		print('Exception message: ' + str(e))
	return positionNumber



list=[]
but=["NONE"]
#MATRIX BUTTONS FN
button=[[1,2,3,'$'],[4,5,6,0],[7,8,9,'%']]
#mmatrix switch fn
def push():
    but[0]="NONE"
    for i in matrO:
        GPIO.output(i,False)
        for j in matrI:
        	if not GPIO.input(j):
        		list.append(i)
        		rw=matrO.index(i)
        		list.append(j)
        		cl=matrI.index(j)
                print(id(but))
                but[0]=button[rw][cl]
                print(id(but))
        list.append("__")
        GPIO.output(i,True)
def main():
    touch=GPIO.input(18)
    stats_disp( not touch)
    fingerfn_disp(touch)
    us=fscanner_disp(touch)
    print (us)
    time.sleep(3)
    usr_disp(touch,us)
    GPIO.output(ledO[4],False)

    push()
    print(list)
    print(but[0])

while True:
    push()
    print("\n" +str(but)+"\n")
    time.sleep(.07)

if touch:
    exit(1)
