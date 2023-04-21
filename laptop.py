import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("appelhan/sensor_data")

    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("appelhan/ipinfo", on_message_from_sensor_data)

"""This object (functions are objects!) serves as the default callback for 
messages received when another node publishes a message this client is 
subscribed to. By "default,"" we mean that this callback is called if a custom 
callback has not been registered using paho-mqtt's message_callback_add()."""
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

#Custom message callback.
def on_message_from_sensor_data(client, userdata, message):
    # Do all the data processing and plotting


if __name__ == '__main__':
    
    #create a client object
    client = mqtt.Client()
    #attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    client.connect(host="68.181.32.115", port=11000, keepalive=60)
    client.loop_forever()