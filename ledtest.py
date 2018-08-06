from gpiozero import LED
from time import sleep

# Raspberry Pi 2 V1.1
# connected pins:
# 5,6,7,8,9,10
# (LED + button)

# GPIO: 9, 7, 15, 16

led = LED(6)

while True:
    print "on"
    led.on()
    sleep(6)
    print "off"
    led.off()
    sleep(6)
    