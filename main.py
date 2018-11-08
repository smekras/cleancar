from time import sleep

import network
from machine import Pin
from neopixel import NeoPixel
from umqtt.simple import MQTTClient

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.ifconfig(("192.168.1.251", "255.255.255.0", "192.168.1.1", "1.1.1.1"))
sta_if.connect("ITEK_f18v", "raspberry")

SERVER = "3.121.31.186"
CLIENT_ID = "gate_check"
TRANSMIT = b"GateCheck"
RECEIVE = b"Control"

c = MQTTClient(CLIENT_ID, SERVER)

button = Pin(2, Pin.IN, Pin.PULL_UP)
led = Pin(0, Pin.OUT)
np = NeoPixel(led, 8)


def change_color(color):
    if color == "green":
        print("LED to green")
        np[0] = (0, 255, 0)
    elif color == "yellow":
        print("LED to yellow")
        np[0] = (255, 80, 0)
    else:
        print("LED to red")
        np[0] = (255, 0, 0)
    np.write()
    r, g, b = np[0]


def send_message(msg):
    c.connect()
    if c.connect():
        print("publishing: ", msg)
        c.publish(TRANSMIT, msg)
        c.disconnect()
    else:
        change_color('red')
        print("could not connect")


def sub_cb(topic, msg):
    if msg == b"open":
        change_color('green')
    elif msg == b"stop":
        change_color('red')
    else:
        change_color('yellow')


c.set_callback(sub_cb)
c.connect()
if c.connect():
    print("connecting to mqtt server")
    c.subscribe(RECEIVE)

change_color('red')

while True:
    if button.value() == 0:
        print("i think i see a car")
        sleep(.01)  # when pressed, button needs 1-2 ms to stabilise to HIGH
        if button.value() == 0:  # check again to avoid false positives
            print("i did! i did see a car!")
            change_color('yellow')
            send_message(b"Car detected")

    c.check_msg()
    sleep(1)
