from time import sleep

import network
from machine import Pin
from neopixel import NeoPixel
from umqtt.simple import MQTTClient

sta_if = network.WLAN(network.STA_IF)
# sta_if.ifconfig(("192.168.1.251", "255.255.255.0", "192.168.1.1", "1.1.1.1"))
# sta_if.connect("ITEK_f18v", "raspberry")
sta_if.connect("smekphone", "svkj9096")

while not sta_if.isconnected():
    pass

if sta_if.isconnected():
    print("Connection Status: ON")
else:
    print("Connection Status: OFF")

button = Pin(2, Pin.IN, Pin.PULL_UP)
led = Pin(0, Pin.OUT)
np = NeoPixel(led, 8)

SERVER = "3.121.31.186"
CLIENT_ID = "gate_check"
TRANSMIT = b"GateCheck"
RECEIVE = b"Control"

c = MQTTClient(CLIENT_ID, SERVER)


def change_color(color):
    if color == "green":
        print("Carwash open")
        np[0] = (0, 255, 0)
    elif color == "yellow":
        print("Checking...")
        np[0] = (255, 80, 0)
    else:
        print("Press to open")
        np[0] = (255, 0, 0)
    np.write()
    r, g, b = np[0]


def send_message(msg):
    print("Please wait...")
    c.publish(TRANSMIT, msg)


def sub_cb(topic, msg):
    if msg == b"open":
        change_color('green')
    elif msg == b"stop":
        change_color('red')
    else:
        change_color('yellow')


c.set_callback(sub_cb)

c.connect()
sleep(2)
print("Connecting to MQTT server")
c.subscribe(RECEIVE)

change_color('red')

while True:
    if button.value() == 0:
        sleep(.1)  # when pressed, button needs 10 ms to stabilise to HIGH
        if button.value() == 0:  # check again to avoid false positives
            print("Car detected")
            change_color('yellow')
            send_message(b"Car detected")

    c.check_msg()
    sleep(1)
