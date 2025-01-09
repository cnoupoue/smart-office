import paho.mqtt.client as mqtt
import time

class MQTT:
    def __init__(self, client_id=None, sub_callback=None, username=None, password=None):
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        self.sub_callback = sub_callback
        
        if username is not None and password is not None:
            self.client.username_pw_set(username=username, password=password)
        
        # Assign default callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_subscribe = self._on_subscribe
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, mqttc, obj, flags, rc):
        """Callback for when the client connects to the broker."""
        print("Connected with result code: {}".format(rc))

    def _on_disconnect(self, mqttc, obj, rc):
        """Callback for when the client disconnects from the broker."""
        print(f"Disconnected with result code: {rc}")

    def _on_message(self, mqttc, obj, msg):
        """Callback for when a message is received."""
        if self.sub_callback:
            self.sub_callback(msg.topic, str(msg.payload.decode('utf-8')))
        else:
            print("received message: " + str(msg.payload))

    def _on_publish(self, mqttc, obj, mid):
        """Callback for when a message is published."""
        # print("Message published - MID: {}".format(mid))

    def _on_subscribe(self, mqttc, obj, mid, granted_qos):
        """Callback for when a subscription is successful."""
        # print("Subscribed - MID: {}, QoS: {}".format(mid, granted_qos))

    def connect(self, url, port, keepalive=60):
        """Connect to the MQTT broker."""
        try:
            self.client.connect(url, port, keepalive=keepalive)
            self.client.loop_start()
        except Exception as e:
            raise e

    def publish(self, topic, value, qos=0):
        """Publish a message to a topic."""
        self.client.publish(topic, value, qos=qos)

    def subscribe(self, topic, qos=0):
        """Subscribe to a topic."""
        self.client.subscribe(topic, qos=qos)
    
    def loop_stop(self):
        self.client.loop_stop()
    
    def disconnect(self):
        self.client.disconnect()


# Example usage:
# mqttc = MQTT(client_id="id1", sub_callback=lambda msg: print(f"Custom callback received: {msg}"), username="your_username", password="your_password")
# mqttc.connect(url="broker.hivemq.com", port=1883)
# mqttc.subscribe(topic="test")
# mqttc.publish(topic="test", value="Hello, MQTT!")
