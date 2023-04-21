import time
import grovepi
#import paho.mqtt.client as mqtt
from datetime import datetime
import socket
import random


# """This function (or "callback") will be executed when this client receives 
# a connection acknowledgement packet response from the server. """
# def on_connect(client, userdata, flags, rc):
#     print("Connected to server (i.e., broker) with result code "+str(rc))



# #get IP address
# ip_address = socket.gethostbyname(socket.gethostname())
# #create a client object
# client = mqtt.Client()
# #attach the on_connect() callback function defined above to the mqtt client
# client.on_connect = on_connect
# client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
# """ask paho-mqtt to spawn a separate thread to handle incoming and outgoing mqtt messages."""
# client.loop_start()
# time.sleep(1)


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

soundsensor_threshold = 10
lightsensor_threshold = 10
ultrasonic_threshold = 10

# def button_interrupt():
#     grovepi.digitalWrite(buzzer, 0)
#     grovepi.digitalWrite(led, 0)


# grovepi.attachInterrupt(button, button_interrupt, "FALLING")

 

while True:
    try:
        

        soundsensor_value = grovepi.analogRead(soundsensor)
        lightsensor_value = grovepi.analogRead(lightsensor)
        range_value = grovepi.ultrasonicRead(ultrasonic_ranger)

        print(soundsensor_value)
        print(lightsensor_value)
        print(range_value)
        

        # Read sensor value from potentiometer
        sensor_value = grovepi.digitalRead(button)


        if((soundsensor_value > soundsensor_threshold) or (lightsensor_value > lightsensor_threshold) or (range_value > ultrasonic_threshold)):
            flag = 1
        

        while(flag == 1):
            #print(grovepi.digitalRead(button))
            if((grovepi.digitalRead(button)) == 1): 
                grovepi.digitalWrite(buzzer, 0)
                grovepi.digitalWrite(led, 0)
                flag = 0
            elif((grovepi.digitalRead(button)) == 0): 
                grovepi.digitalWrite(buzzer, 1)
                grovepi.digitalWrite(led, 1)
                time.sleep(0.5)

                grovepi.digitalWrite(led, 0)
                time.sleep(0.5)

            
    

    except KeyboardInterrupt:
        grovepi.analogWrite(led,0)
        break
    except IOError:
       print ("Error")

    except Exception as e:
       print ("Error:{}".format(e))

    time.sleep(0.1) # don't overload the i2c bus
        



    # #publish date and time in their own topics
    # client.publish("appelhan/time", f"{time_data}")
    # print("Publishing time")

    # client.publish("appelhan/date", f"{date}")
    # print("Publishing date")