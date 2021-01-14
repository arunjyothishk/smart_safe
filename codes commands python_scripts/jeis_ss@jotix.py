
"""
 ============================================================================
 Name        :jeis_ss@jotix.py

 Author      : ARUN JYOTHISH  K
 Version     :v1.0		| 12/12/2018 4:50 pm
 Copyright   : "Smart Safe" Open Source
 Description : Smart safe project, secure locker system including iot,finger
  	  	  	  print,speech synthesis,display,pin code,using raspberry pi
 ============================================================================
 """

import Adafruit_SSD1306
import time
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

matrO=[22,27,17]
matrI=[10,9,11,5]
fngrI=[18]
mot=[23,24,25,8]
ledO=[26,19,16,20,6,21]

op=ledO+matrO+fngrI+mot
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
	log('Exception message: ' + str(e))
	exit(1)

GPIO.output(ledO[0],True)

import subprocess

RST = None

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
un = 0
# Load default font.
font = ImageFont.load_default()

#some global variable
prc=[""]
tmp=[""]
pos=-1
positionNumber = -1
us=[-1]
l2=30
l22=15
usrname=['jyothish k','Arun k','Ashwin c','Vyshak ms','jishal p','shanid p','shibil p','Rishad Babu','Sadhique Ali','jijesh kp',"Unknown..!"]
name=['jo','ar','as','vy','ji','sh','sp','ri','sa','jk','un']
mailaddresses=["arunjyothishvikku@gmail.com",
                "arunkvnb738@gmail.com",
                "ashwinkrishna62@gmail.com",
                "jishalarimbra@gmail.com",
                "cheekodeshand@gmail.com",
                "shibi4702@gmail.com",
                "vysakhms2016@gmail.com",
                "rishadbaburkz@gmail.com",
                "sadhiquealichulliyil404@gmail.com",
                "jijeshkpj@gmail.com"
                ]
password=["0010","7623","1122","8976","6452","0912","6104","8959","1324","8546","7483"]

def voice(file):
    log("voice : "+file)
    cmd="omxplayer /home/pi/project/Audio/voice_clip_"
    cmd+=file+".mp3"
    process=subprocess.call(cmd,shell=True)
    time.sleep(.03)
#    print(file+" playing status  : "+process)

def mailaddr(type):
#    print("mailaddr usrname us[0]  : "+usrname[us[0]])
    Time=datetime.datetime.now().replace(microsecond=0).time()
    Date=datetime.datetime.now().date()

    for addr in mailaddresses:
        if type=="unknown":
#            print("mailaddr if excecuted")

            cmd= "echo \" Smart Safe , Detected an Unknown  \'UNLOCK\' Attempt \n \n"
            cmd+="Date : " +str(Date)+"\nTime : "+str(Time)+"\n \n ___ JEIS ROBOTICS\" | mail -s \" SMART SAFE SECURITY ALERT ! \" "
            cmd+=addr
            cmd+=" & "
        elif type=="login":
#            print("mailaddr elif excecuted")
            cmd= "echo \" Smart Safe ,  "
            cmd+=str.upper(usrname[us[0]])
            cmd+="  logged in \n \n"
            cmd+="Date : "+str(Date)+"\nTime : "+str(Time)+" \n \n ___ JEIS ROBOTICS\" | mail -s \" SMART SAFE LOG IN ALERT ! \" "
            cmd+=addr
            cmd+=" & "
        else:
            pass
#            print("mailaddr else excecuted")
        mail_cmd=subprocess.call(cmd,shell=True)
        log(mail_cmd)


def stats_disp(k):
    if k == False:
        return
    else:
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
    else:
        voice("scfp")
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
       # print("value of top",top)
        draw.text((x, 15),       "S C A N N I N G... " ,  font=font, fill=255)
        draw.text((x+15, l2),     "fingerprint..../", font=font, fill=255)
        draw.text((x, l2+16),   "Tmpl/$."+ str(f.getTemplateCount()),  font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.3)


def grnt_disp(k):
    if k == False:
        return
    else:
        voice("accgrnt")
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
    else:
        voice("accdenied")
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

    else:
        voice("succ")
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
    else:
        voice("failed")
        voice("unknown")
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, 15),       "F A I L E D .... " ,  font=font, fill=255)
        draw.text((x+15, l2),     "No usr match found.", font=font, fill=255)
        GPIO.output(ledO[2],True)
        disp.image(image)
        disp.display()

        try:
            cmd="python /home/pi/mail_alert.py &"
            mail_alert=subprocess.call(cmd,shell=True)
#            print(mail_alert)
            time.sleep(.1)
        except Exception as e:
            log("Can not send mall_alert : "+str(e))


def usr_disp(k,pos):
    if k == False:
        return
    else:
        if not pos==-1 :
            mailaddr("login")
            voice("wl")
            voice(name[pos])
        else:
            mailaddr("unknown")

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
        time.sleep(.4)

def iot_disp(k,pos):
    if k == False:
        return
    else:
        voice("iot")
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
    else:
        voice("plsveri")
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, 0),       "E N T E R __P I N " ,  font=font, fill=255)
        draw.text((x, l22),     str(usrname[pos])+"@ : ", font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)

maskeyCount=[5]
def maskey(k):
    if k:
        maskeyCount[0]+=20
#        print(maskeyCount)
        v=35
        x=maskeyCount[0]
        draw.text((x, v),    " "+prc[0] , font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)
    else:
        pass



def unlocked_disp(k):
    if k == False:
        return
    else:
        voice("unl")
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, 15),       "U N L O C K E D /... " ,  font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)

def locking_disp(k):
    if k == False:
        return
    else:
        voice("loc")
        draw.rectangle((0,0,width,height),outline=0,fill=0)
        draw.text((x,15),"L O C K I N G /...",font=font,fill=255)
        disp.image(image)
        disp.display()
        time.sleep(.1)

def fscanner_disp(k):
    if k == False:
        return -1
    else:
    	templates=str(f.getTemplateCount())
    	storageof=str(f.getStorageCapacity())
    	## Gets some sensor information
#    	print('Currently used templates: ' + templates +'/'+ storageof )
    	## Tries to search the finger and calculate hash
    	try:
    		log('Waiting for finger...')

    		## Wait that finger is read
            while ( f.readImage() == False ):
                print ("in fingerprint scanning waiting")
                pass
    		## Converts read image to characteristics and stores it in charbuffer 1
    		f.convertImage(0x01)
               ## Searchs template
    		result = f.searchTemplate()

    		positionNumber = result[0]
    		accuracyScore = result[1]
#    		log("match found")
    		if ( positionNumber == -1 ):
    			log('No match found!')
    			failed_disp(1)
    		else:
    			passed_disp(1)
    			log('Found template at position #' + str(positionNumber))
#    			print('The accuracy score is: ' + str(accuracyScore))

    		## OPTIONAL stuff
    	except Exception as e:
    		log('Operation failed!')
    		log('Exception message: ' + str(e))
    	return positionNumber



list=[]
but=["NONE"]
#MATRIX BUTTONS FN
button=[[1,2,3,'$'],[4,5,6,0],[7,8,9,'%']]
#mmatrix switch fn
def push():
    rw=0
    cl=0
    but[0]="NONE"
    for i in matrO:
        GPIO.output(i,False)
        for j in matrI:
            if not GPIO.input(j):
#                list.append(i)
                rw=matrO.index(i)
#                list.append(j)
                cl=matrI.index(j)
                but[0]=button[rw][cl]
            else:
                pass

    #        list.append("__")
        GPIO.output(i,True)
def MOT(k,j):

    if k=="latch":
        if j=="forward":
            GPIO.output(23,True)
            GPIO.output(25,False)
        elif j=="reverse":
            GPIO.output(23,False)
            GPIO.output(25,True)
        else:
            GPIO.output(23,False)
            GPIO.output(25,False)
    else:
        pass

    if k=="slide":
        if j=="forward":
            GPIO.output(24,True)
            GPIO.output(8,False)
        elif j=="reverse":
            GPIO.output(24,False)
            GPIO.output(8,True)
        else:
            GPIO.output(24,False)
            GPIO.output(8,False)
    else:
        pass

def unl(k):
    if k:
        MOT("latch","reverse")
        grnt_disp(True)
        time.sleep(.5)
        MOT("slide","reverse")
        unlocked_disp(True)
        time.sleep(2)
        MOT("latch","")
        MOT("slide","")
    else:
        pass

    while True:
        push()
        if but[0]=="%":
            MOT("slide","forward")
            locking_disp(True)
            time.sleep(.5)
            MOT("latch","forward")
            time.sleep(2)
            MOT("latch","")
            MOT("slide","")
            voice("clsd")
            return main()
        else:
            pass
def log(para):
    if not tmp[0]==para:
        date_time=datetime.datetime.now()
        tmp[0]=para
        print(para)
        log=open("log.txt","a")
        log.write("\n\n"+str(date_time)+" :     "+str(para)+"\n")
        log.close()
    else:
        pass

def main():
    prc[0]=""
#    print(us[0])
    Tries=3
    touch=GPIO.input(18)
    stats_disp( not touch )
    fingerfn_disp(touch)
    if touch:
        us[0]=fscanner_disp(touch)
    else:
        pass
#    print(but[0])
#    time.sleep(.3)
    usr_disp(touch,us[0])
#    time.sleep(.3)
#    print(us[0])
    line=" User logged in: " +usrname[us[0]]
    log(line)
    if usrname[us[0]]=="Unknown..!":
        return run()
    else:
        while Tries:
            log("Tries loop running: "+str(Tries))
            push()
            pin=4
            if but[0]=="%":
                us[0]=-1
                break
            elif but[0]=="$":
#                print ("ok button")
                Tries-=1
                psk=""
                pin_disp(True,us[0])
                while pin:
#                    print("pin digits: "+str(pin))
                    push()
                    if but[0]=="%":
                        break
                    else:
                        if not but[0]=="NONE":
                            pin-=1
                            prc[0]=str(but[0])
                            psk+=prc[0]
#                            print("Enter code : "+psk)
                            maskey(True)
                        else:
#                            print("else excecuted")
                            pass
                    log("psk ip: "+psk)
                    pswd=password[us[0]]
#                    print("password set: " +pswd)
                if psk==pswd:
                    log("Code matched ..")
                    unl(True)
                    continue
                else:
                    log("Code error !")
                    denied_disp(True)
                    time.sleep(.3)
#                    print("Try..failed")
                    maskeyCount[0]=5
                    pin_disp(True,us[0])
                    pin=4
                    continue
            else:
                pass
        log("Attempt Exceeded !")
        us[0]=-1

def run():
#    print("run function ")
    while 1:

        try:
            cmd="python /home/pi/sub.py"
            mail_recieve=subprocess.call(cmd,shell=True)
        except Exception as e:
#            print("Can not recieve command from mail : "+str(e))
            pass

        main()

run()

"""
Smart Safe security Locker
Source code:
                        programmed by Arun jyothish k

"""
