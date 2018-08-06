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
ledch = 16 # 10 15 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledch, GPIO.OUT)
print "ON"
GPIO.output(ledch,GPIO.HIGH)
time.sleep(3)
print "OFF"
GPIO.output(ledch,GPIO.LOW)



GPIO.setmode(GPIO.BOARD)
GPIO.setup(ch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(ch,GPIO.RISING,callback=cb)
message = input("Pres Enter to stop")

GPIO.cleanup()