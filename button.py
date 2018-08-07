import RPi.GPIO as GPIO
import time

def cb(channel):
    print("pressed") 

print "start"

ch = 5

# INPUT BUTT = 5!!!!

GPIO.setwarnings(False)



# LED test__
print "LED"
ledch = 7 # 10 15 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledch, GPIO.OUT)
print "ON %s" % ledch
GPIO.output(ledch,GPIO.HIGH)
time.sleep(1)
print "OFF"
GPIO.output(ledch,GPIO.LOW)
time.sleep(1)
GPIO.cleanup()