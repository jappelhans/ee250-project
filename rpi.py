import time
import grovepi
import paho.mqtt.client as mqtt
from datetime import datetime
import socket
import random


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
client.connect(host="172.20.10.5", port=1883, keepalive=60)
"""ask paho-mqtt to spawn a separate thread to handle incoming and outgoing mqtt messages."""
client.loop_start()
time.sleep(1)

#client.publish("security/sensor_data", "test string")

soundsensor = 1

# light sensor connected to analog port A2
lightsensor = 2

# Connect the LED to digital port D3
# SIG,NC,VCC,GND
led = 3

button = 6

buzzer = 4


# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 5

grovepi.pinMode(soundsensor,"INPUT")
grovepi.pinMode(lightsensor,"INPUT")
grovepi.pinMode(ultrasonic_ranger,"INPUT")
grovepi.pinMode(led,"OUTPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(buzzer,"OUTPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

lightsensor_threshold = 100
soundsensor_threshold = 200
ultrasonic_threshold = 100


buzzer_value = 0

while True:
    try:
        

        soundsensor_value = grovepi.analogRead(soundsensor)
        lightsensor_value = grovepi.analogRead(lightsensor)
        range_value = grovepi.ultrasonicRead(ultrasonic_ranger)
        while (range_value > 1000):
            range_value = grovepi.ultrasonicRead(ultrasonic_ranger)

        print(lightsensor_value)
        print(soundsensor_value)
        print(range_value)
        print(buzzer_value)
        

        # trigger the alarm
        if(((soundsensor_value > soundsensor_threshold) or (lightsensor_value > lightsensor_threshold) or (range_value > ultrasonic_threshold)) and ((grovepi.digitalRead(button)) == 0)):
            # flag = 1
            grovepi.digitalWrite(buzzer, 1)
            buzzer_value = 1

        if((grovepi.digitalRead(button)) == 1): 
            grovepi.digitalWrite(buzzer, 0)
            # grovepi.digitalWrite(led, 0)
            buzzer_value = 0
            # flag = 0

        

        #light, sound, distance, alarm
        sensor_data_values = str(lightsensor_value) + " " + str(soundsensor_value) + " " + str(range_value) + " " + str(buzzer_value)
        #publish date and time in their own topics
        client.publish("security/sensor_data", sensor_data_values)
        print("Publishing sensor data")
        time.sleep(0.2)

        
    except KeyboardInterrupt:
        grovepi.analogWrite(led,0)
        break
    except IOError:
       print ("Error")

    except Exception as e:
       print ("Error:{}".format(e))

    time.sleep(0.1) # don't overload the i2c bus
        



    