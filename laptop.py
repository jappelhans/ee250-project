import paho.mqtt.client as mqtt
import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import random
import time
import threading

updated = 0
message_buffer = []

# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
# fig = figure(num = 0, figsize = (5, 5))#, dpi = 100)
fig = figure()
fig.suptitle("Sensor Monitoring Plots", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))
ax02 = subplot2grid((2, 2), (0, 1))
# ax03 = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
ax03 = subplot2grid((2, 2), (1, 0))
ax04 = subplot2grid((2,2), (1, 1))
tight_layout()

# Set titles of subplots
ax01.set_title('Light Measurements')
ax02.set_title('Sound Measurements')
ax03.set_title('Rangefinder Measurements')
ax04.set_title('Alarm Status')

# set y-limits
ax01.set_ylim(0,1023)
ax02.set_ylim(0,1023)
ax03.set_ylim(0,1023)
ax04.set_ylim(0,2)

# set x-limits
ax01.set_xlim(0,50.0)
ax02.set_xlim(0,50.0)
ax03.set_xlim(0,50.0)
ax04.set_xlim(0,50.0)

# Turn on grids
ax01.grid(True)
ax02.grid(True)
ax03.grid(True)
ax04.grid(True)

# set label names
ax01.set_xlabel("time (seconds)")
ax01.set_ylabel("Light Intensity")
ax02.set_xlabel("time (seconds)")
ax02.set_ylabel("Sound Intensity")
ax03.set_xlabel("time (seconds)")
ax03.set_ylabel("Distance")
ax04.set_xlabel("time (seconds)")
ax04.set_ylabel("Status (On/Off)")

# Data Placeholders
light_data = []
sound_data = []
range_data = []
alarm_data = []
t = []
light_thresh = []
sound_thresh = []
range_thresh = []


# set plots
light_plot, = ax01.plot(t,light_data,'b-', label="light data")
light_thresh_plot, = ax01.plot(t,light_thresh,'r-', label="light threshold")

sound_plot, = ax02.plot(t,sound_data,'b-', label="sound data")
sound_thresh_plot, = ax02.plot(t,sound_thresh, '-r', label="sound threshold")

range_plot, = ax03.plot(t,range_data,'b-', label="range data")
range_thresh_plot, = ax03.plot(t,range_thresh, '-r', label="range threshold")

alarm_plot, = ax04.plot(t,alarm_data,'b-', label="alarm data")

# set legends
ax01.legend([light_plot,light_thresh_plot], [light_plot.get_label(),light_thresh_plot.get_label()])
ax02.legend([sound_plot,sound_thresh_plot], [sound_plot.get_label(),sound_thresh_plot.get_label()])
ax03.legend([range_plot,range_thresh_plot], [range_plot.get_label(),range_thresh_plot.get_label()])

# Data Update
xmin = 0.0
xmax = 50.0
x = 0.0


def updateData(self):
    global x
    global light_data
    global light_thresh
    global sound_data
    global sound_thresh
    global range_data
    global range_thresh
    global alarm_data
    global t

    # print ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    # tmpp1 = 1 + exp(-x) *sin(2 * pi * x)
    # tmpv1 = - exp(-x) * sin(2 * pi * x) + exp(-x) * cos(2 * pi * x) * 2 * pi
    # temp1 = random.random()
    # temp2 = random.random()

    # light_data.append(temp1)
    # sound_data.append(temp2)
    # range_data.append(0.5*temp1)
    # alarm_data.append(0.5*temp2)

    global message_buffer
    string_with_numbers = str(message_buffer[-1].payload, "utf-8")
    numbers_list = [int(num) for num in string_with_numbers.split()]
    light_data.append(numbers_list[0])
    sound_data.append(numbers_list[1])
    range_data.append(numbers_list[2])
    alarm_data.append(numbers_list[3])   

    t.append(x)
    # Set the threshold values ##################################################################################################
    light_thresh.append(100)
    sound_thresh.append(200)
    range_thresh.append(100)

    # print(light_data)
    # print(light_thresh)
    # print(t)

    x += 0.5

    light_data = light_data[-500:]
    sound_data = sound_data[-500:]
    range_data = range_data[-500:]
    alarm_data = alarm_data[-500:]
    t = t[-500:]
    light_thresh = light_thresh[-500:]
    sound_thresh = sound_thresh[-500:]
    range_thresh = range_thresh[-500:]


    light_plot.set_data(t,light_data)
    light_thresh_plot.set_data(t,light_thresh)
    sound_plot.set_data(t,sound_data)
    sound_thresh_plot.set_data(t, sound_thresh)
    range_plot.set_data(t,range_data)
    range_thresh_plot.set_data(t, range_thresh)
    alarm_plot.set_data(t,alarm_data)

    if x >= xmax-1.00:
        light_plot.axes.set_xlim(x-xmax+1.0,x+10.0)
        sound_plot.axes.set_xlim(x-xmax+1.0,x+10.0)
        range_plot.axes.set_xlim(x-xmax+1.0,x+10.0)
        alarm_plot.axes.set_xlim(x-xmax+1.0,x+10.0)

    global updated
    updated = 1
    return light_plot, light_thresh_plot, sound_plot, sound_thresh_plot, range_plot, range_thresh_plot, alarm_plot



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("security/sensor_data")

    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("security/sensor_data", on_message_from_sensor_data)

"""This object (functions are objects!) serves as the default callback for 
messages received when another node publishes a message this client is 
subscribed to. By "default,"" we mean that this callback is called if a custom 
callback has not been registered using paho-mqtt's message_callback_add()."""
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

#Custom message callback.
def on_message_from_sensor_data(client, userdata, msg):
    global message_buffer
    message_buffer.append(msg)
    # string_with_numbers = str(msg.payload, "utf-8")
    # numbers_list = [int(num) for num in string_with_numbers.split()]
    # global light_data
    # global sound_data
    # global range_data
    # global alarm_data
    # light_data.append(numbers_list[0])
    # sound_data.append(numbers_list[1])
    # range_data.append(numbers_list[2])
    # alarm_data.append(numbers_list[3])
    # print(light_data)
    # global updated
    # updated = 0
    # while (updated == 0):
    #     # empty
    #     a = 2



def run_mqtt_loop():
    #create a client object
    client = mqtt.Client()
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect    

    client.connect(host="172.20.10.5", port=1883, keepalive=60)

    client.loop_forever()


if __name__ == '__main__':
    # #create a client object
    # client = mqtt.Client()
    # #attach a default callback which we defined above for incoming mqtt messages
    # client.on_message = on_message
    # #attach the on_connect() callback function defined above to the mqtt client
    # client.on_connect = on_connect

    # client.connect(host="172.20.10.5", port=1883, keepalive=60)

    # client.loop_forever()

    mqtt_thread = threading.Thread(target=run_mqtt_loop)
    mqtt_thread.start()
    time.sleep(1)
    
    simulation = animation.FuncAnimation(fig, updateData, blit=False, frames=None, interval=500, repeat=False)
    plt.show()

    


