import cayenne.client
import time
import logging
import socket
# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "c9ade6c0-5fb4-11e9-81a2-d1fdd4219210"
MQTT_PASSWORD  = "8c679b60ab5e37820b41bce8e4bbf0ab672f968a"
MQTT_CLIENT_ID = "d37820f0-5fb7-11e9-bb1a-97096e6377d3"
s = socket.socket()
# The callback for when a message is received from Cayenne.
def on_message(message):
    print("message received: " + str(message))
    # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)


while True:
    s = socket.socket()
    s.connect(('192.168.1.150', 1313))
    s.sendall('lamp,myRoom,getState'.encode())
    res = s.recv(8)
    res = res.decode()
    if res == 'True':
        res = 1
    else:
        res = 0
    print(res)
    s.close()
    print(client.getDataTopic(1))
    client.mqttPublish(client.getDataTopic(1), 'DIGITAL,d={}'.format(res))
    time.sleep(1)
