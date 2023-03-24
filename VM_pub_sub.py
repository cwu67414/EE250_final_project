"""EE 250L Lab 04 Starter Code
Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
import REST_new
from FuzzyControl import Fuzzy


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("wangsiya/lcd")
    client.subscribe("wangsiya/led")
    client.subscribe("wangsiya/waterlevel")
    client.message_callback_add("wangsiya/waterlevel", water_callback)

def water_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("WL: "+ str(message.payload, "utf-8") + " cm")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def weather(user_zip):
    fuz = Fuzzy()
    fuz.update_sun(REST_new.weather_init(user_zip)[0], REST_new.weather_init(user_zip)[1])
    fuz.update_data(REST_new.weather_init(user_zip)[2], REST_new.weather_init(user_zip)[3], REST_new.weather_init(user_zip)[4])
    fuz.de_fuzz()
    client.publish("wangsiya/led", fuz.led_out)
    lcd_string = str(REST_new.weather_init(user_zip)[2])+'\n'+str(REST_new.weather_init(user_zip)[3])
    client.publish("wangsiya/lcd", lcd_string)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    #setup the weather listener
    try:
        user_zip = int(input('ZIP:'))
    except ValueError:
        print("Not a number")
    while True:
        time.sleep(1)
        weather(user_zip)