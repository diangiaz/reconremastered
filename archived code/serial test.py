from threading import Thread
import serial
from time import sleep

serialPort1 = serial.Serial("COM4", 9600)

class Receiver1(Thread):
		def __init__(self, serialPort1): 
			Thread.__init__(self) 
			self.serialPort = serialPort1
		def run(self):
			global serialPort1
			global strBuilder1
			text = "" 
			while (text != "exitReceiverThread\n"): 
				text = serialPort1.readline()
				print("serial output: " + text.decode())
			
			self.serialPort.close()
			
receive = Receiver1(serialPort1) 
receive.start()

def Sender():
	global serialPort1
	
	while True:
		serialPort1.flushInput()
		text = input("") + "\n"
		serialPort1.write(text.encode('utf-8'))
		bytes_to_read = serialPort1.inWaiting()
		sleep(.2)

sSend = Thread(target=Sender)
sSend.start()
