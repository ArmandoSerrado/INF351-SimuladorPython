import paho.mqtt.client as mqtt
import pygame, sys
from pygame.locals import *
import array


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$INF351/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()

pygame.init()
display = pygame.display.set_mode((200,200),0,32)
clock = pygame.time.Clock()
client.loop_start()

_payload = 0
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                _payload = 1
            elif event.key == pygame.K_DOWN:
                _payload = 2
            elif event.key == pygame.K_LEFT:
                _payload = 3
            elif event.key == pygame.K_RIGHT:
                _payload = 4
            elif event.key == pygame.K_r:
                _payload = 5
            elif event.key == pygame.K_p:
                _payload = 6
            else:
                _payload = 0

            client.publish("$INF351/EVENT", payload=_payload.to_bytes(1, 'little'))

client.loop_stop()

