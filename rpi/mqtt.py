import context
import paho.mqtt.client as mqtt

value = None

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    # print("mid: " + str(mid))
    print("value: " + str(value))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client("prefix2")
mqttc.username_pw_set(username='user2', password='user2')
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log

def connect(url, port):
    mqttc.connect(url, port, 60)
    mqttc.loop_start()
    
def publish(topic, value):
    infot = mqttc.publish(topic, value, qos=2)
#    infot.wait_for_publish()
    
# 
# (rc, mid) = mqttc.publish("topic1", "bar", qos=2)
#print(str(rc) + ':' + str(mid) + ':' + str(infot))

