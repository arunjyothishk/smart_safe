import subprocess
import Adafruit_SSD1306
import time
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import hashlib


print(" starting...program..")

cmd = "python /home/pi/jeis_ss@jotix.py"

err=subprocess.call(cmd,shell=True)

print(err)

cmd = " omxplayer /home/pi/project/Audio/voice_clip_errordtct.mp3"
subprocess.call(cmd,shell=True)

RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
font = ImageFont.load_default()
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
draw.text((0, 5),  "Error Detected !",  font=font, fill=255)
draw.text((0, 20),  "Rebooting System ",  font=font, fill=255)
draw.text((10, 40),  "in 10 seconds... ",  font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(10)
cmd="sudo reboot now"
#subprocess.call(cmd,shell=True)
