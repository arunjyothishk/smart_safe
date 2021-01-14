import RPi.GPIO as gpio
import picamera
import time

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

fromaddr = "jeisdevice0@gmail.com"
toaddr = "arunjyothishvikku@gmail.com"

mail = MIMEMultipart()

mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "Security Alert"
body = "Unknown Attempt Detected.."

HIGH=1
LOW=0
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
data=""

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
    server.login(fromaddr, "jyothujyothu")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def capture_image():
    camera = picamera.PiCamera()
    camera.rotation=180
    camera.awb_mode= 'auto'
    camera.brightness=55

    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print data
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)



#capture_image()
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "jyothujyothu")
text = mail.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
