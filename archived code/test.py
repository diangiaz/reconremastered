from serial import *
from time import sleep
from threading import Thread

readState = False
serialPort = Serial("COM4", 9600)
strBuilder = ""
varCurr = ""
varPrev = ""

# def Receiver():
	# global readState
	# global serialPort
	# global strBuilder
	# global varCurr
	# global varPrev
	
	# while True:
		# varPrev = varCurr
		# serialRead = serialPort.read()
		# varCurr = serialRead.decode()
	
		# if readState == False:
			# readState = True
			# strBuilder = ""
	
		# elif readState == True:
			# text = serialPort.readline()
			# strBuilder += text.decode()
			# print(text.decode())
			
class Receiver(Thread):
		def __init__(self, serialPort): 
			Thread.__init__(self) 
			self.serialPort = serialPort 
		def run(self):
			global serialPort
			text = "" 
			while (text != "exitThread\n"): 
				text = serialPort.readline()
				print (text.decode())
			
			self.serialPort.close() 
			
def Sender():
	global serialPort
	
	while True:
		serialPort.flushInput()
		text = input("") + "\n"
		serialPort.write(text.encode('utf-8'))
		bytes_to_read = serialPort.inWaiting()
		sleep(.2)	
			
			
# class Sender(Thread):
    # global serialPort
    # def __init__(self, serialPort): 
        # Thread.__init__(self) 
        # self.serialPort = serialPort 
    # def run(self):
        # global serialPort
        # text = "" 
        # while(text != "exitThread\n"):
            # serialPort.flushInput()
            # text = input("") + "\n" 
            # self.serialPort.write(text.encode('utf-8'))
            # bytes_to_read = serialPort.inWaiting()
            # sleep(.2)
        # self.serialPort.close()
        

# send = Sender(serialPort) 
# send.start()

receive = Receiver(serialPort) 
receive.start()

# sRead = Thread(target=Receiver)
# sRead.start()

sSend = Thread(target=Sender)
sSend.start()
