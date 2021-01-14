
import datetime

fcopy=input("Enter the file name you want to copy : ")
readfile=open(fcopy)
readcontents=readfile.read()
readfile.close()
namewrite=datetime.datetime.now()

writefile=open(fcopy+"-copy.py","w")
writefile.write(readcontents+"#"+str(namewrite))
writefile.close()
print("success!")
