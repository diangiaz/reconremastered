from serial import *
from time import sleep
from threading import Thread 

class Receiver(Thread):
    global serialPort
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

class Sender(Thread):
    global serialPort
    def __init__(self, serialPort): 
        Thread.__init__(self) 
        self.serialPort = serialPort 
    def run(self):
        global serialPort
        text = "" 
        while(text != "exitThread\n"):
            serialPort.flushInput()
            text = input("") + "\n" 
            self.serialPort.write(text.encode('utf-8'))
            bytes_to_read = serialPort.inWaiting()
            sleep(.5)
        self.serialPort.close() 

serialPort = Serial("COM3", 9600)

send = Sender(serialPort) 
receive = Receiver(serialPort) 
send.start() 
receive.start()
