import paho.mqtt.client as mq


class MQTTClient(object):
    def __init__(self, name):
        self.client = mq.Client(name)
        self.msg = ""

    def connect(self, address="3.121.31.186"):
        self.client.connect(address)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_message(self, client, userdata, message):
        self.msg = message.payload.decode("utf-8")

    def publish(self, topic="Control", msg="...---..."):
        self.client.publish(topic, msg)

    def subscribe(self, topic="GateCheck"):
        self.client.subscribe(topic)
        self.client.on_message = self.on_message
