from kafka import KafkaConsumer

import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)
    pass
def on_unsubscribe(client, userdata, mid, granted_qos):
    print("On unSubscribed: qos = %d" % granted_qos)
    pass
def on_publish(client, userdata, mid):
    print("On onPublish: qos = %d" % mid)
    pass
def on_disconnect(client, userdata, rc):
    print("Unexpected disconnection rc = " + str(rc))
    pass
 
def start_consumer(client):
    consumer = KafkaConsumer('count', bootstrap_servers = '192.168.35.179:12001')
    for msg in consumer:
        print(msg)
        print("topic = %s" % msg.topic) # topic default is string
        print("partition = %d" % msg.offset)
        print("value = %s" % msg.value.decode()) # bytes to string
        print("timestamp = %d" % msg.timestamp)
        print("time = ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( msg.timestamp/1000 )) )
        client.publish(topic='baby/face',payload=msg.value.decode(),qos=0,retain=False)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_unsubscribe = on_unsubscribe
    client.on_subscribe = on_subscribe
    client.connect('192.168.35.179', 31002) # 600为keepalive的时间间隔
    start_consumer(client)
