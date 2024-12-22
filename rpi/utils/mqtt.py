import paho.mqtt.client as mqtt
from typing import Callable

class MQTT:
    def __init__(self, client_id, sub_callback : Callable[[str], None], username = None, password = None):
        self.client = mqtt.Client(client_id)
        self.sub_callback = sub_callback
        
        if username is not None:
            self.client.username_pw_set(username=username, password=password)
        
        # Assign default callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
    def _on_connect(self, mqttc, obj, flags, rc):
        """Callback for when the client connects to the broker."""
        print("Connected with result code: {}".format(rc))

    def _on_message(self, mqttc, obj, msg):
        """Callback for when a message is received."""
        if self.sub_callback:
            self.sub_callback(str(msg.payload))
        else:
            print("Message received - Topic: {}, QoS: {}, Payload: {}".format(
                msg.topic, msg.qos, str(msg.payload)))

    def _on_publish(self, mqttc, obj, mid):
        """Callback for when a message is published."""
        print("Message published - MID: {}".format(mid))

    def _on_subscribe(self, mqttc, obj, mid, granted_qos):
        """Callback for when a subscription is successful."""
        print("Subscribed - MID: {}, QoS: {}".format(mid, granted_qos))

    def _on_log(self, mqttc, obj, level, string):
        """Optional callback for logging."""
        #print("Log: {}".format(string))

    def connect(self, url, port):
        self.client.connect(url, port, keepalive=60)
        self.client.loop_start()

    def publish(self, topic, value, qos=2):
        infot = self.client.publish(topic, value, qos=qos)
        infot.wait_for_publish()  # Optional: Wait until the message is sent
        print("Published to {}: {} with QoS {}".format(topic, value, qos))

    def subscribe(self, topic, qos=2):
        self.client.subscribe(topic, qos=qos)
        print("Subscribed to {} with QoS {}".format(topic, qos))

    def set_logging(self, enable):
        """
        Enable or disable logging for debugging.

        :param enable: Boolean flag to enable or disable logging
        """
        if enable:
            self.client.on_log = self._on_log
        else:
            self.client.on_log = None

    def set_subscribe_action(self, function):
        self.client.on_subscribe = function


# Example
# mqttc = MQTT(client_id="id1", username="pi", password="hepl")
# mqttc.connect(url="broker.hivemq.com", port=1883)
# mqttc.subscribe(topic="test")
# mqttc.publish(topic="test", value="Hello, MQTT!")
