import subprocess
cmd="omxplayer /home/pi/project/Audio/voice_clip_wlss.mp3"
wlss=subprocess.call(cmd,shell=True)
print(wlss)
