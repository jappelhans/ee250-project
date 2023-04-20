import time
import grovepi
import paho.mqtt.client as mqtt
from datetime import datetime
import socket

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))



#get IP address
ip_address = socket.gethostbyname(socket.gethostname())
#create a client object
client = mqtt.Client()
#attach the on_connect() callback function defined above to the mqtt client
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
"""ask paho-mqtt to spawn a separate thread to handle incoming and outgoing mqtt messages."""
client.loop_start()
time.sleep(1)

while True:


    # Grovepi sensor data reading













    #publish date and time in their own topics
    client.publish("appelhan/time", f"{time_data}")
    print("Publishing time")

    client.publish("appelhan/date", f"{date}")
    print("Publishing date")