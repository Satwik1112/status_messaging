import ssl
from contextlib import asynccontextmanager

from config import configs
import paho.mqtt.client as mqtt
from random import randrange

configs.update({
    'topic': "status"
})


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to {configs['host']}")
        client.subscribe(configs["topic"], 0)
    else:
        print(f"Connection failed with result code {rc} {mqtt.error_string(rc)}")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


client_id = f"mqtt-{randrange(1, 100)}"
mqtt_client = mqtt.Client(
    client_id=client_id,
    protocol=mqtt.MQTTv311
)


def start_mqtt():
    print('Connecting to MQTT host {}:{}.'.format(configs['host'], configs['port']), flush=True)
    mqtt_client.loop_start()
    mqtt_client.connect(configs['host'], configs['port'], 10)
    mqtt_client.username_pw_set(configs['username'], configs['password'])
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_publish = on_publish
    mqtt_client.on_subscribe = on_subscribe
