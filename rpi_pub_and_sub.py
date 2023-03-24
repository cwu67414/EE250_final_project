from pydoc import cli
import paho.mqtt.client as mqtt
import time
import sys
import time
import grovepi
from grove_rgb_lcd import *

sys.path.append('Dexter/GrovePi/Software/Python/')
sys.path.append('Dexter/GrovePi/Software/Python/grove_rgb_lcd')


def led_duty_cyc_control(cycle_pct, pin_num):
    period = 0.01  # second
    on_period = cycle_pct * period
    off_period = period - on_period
    while True:
        grovepi.digitalWrite(pin_num, 1)
        time.sleep(on_period)
        grovepi.digitalWrite(pin_num, 0)
        time.sleep(off_period)


def led_callback(client, userdata, message):
    # the third argument is 'message' here unlike 'msg' in on_message
    led_instruct = float(str(message.payload, "utf-8"))
    print("LED Control: " + message.topic + " " + led_instruct)
    if led_instruct >= 0:
        led_duty_cyc_control(led_instruct, 4)  # write duty cycle sig to pin 4
    else:
        print("Error: command: duty cycle not recongnized.")


def lcd_callback(client, userdata, message):
    # the third argument is 'message' here unlike 'msg' in on_message
    lcd_msg = str(message.payload, "utf-8")
    print("LED Control: " + message.topic + " " + lcd_msg)
    setText_norefresh(lcd_msg)


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))
    # subscribe to topics of interest here
    client.subscribe("wangsiya/led")
    client.message_callback_add("wangsiya/led", led_callback)
    client.subscribe("wangsiya/lcd")
    client.message_callback_add("wangsiya/lcd", lcd_callback)


def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


if __name__ == '__main__':
    # this section is covered in publisher_and_subscriber_example.py
    setText("Smart Terrarium\n    Start!")
    setRGB(16, 64, 192)
    time.sleep(2)
    setText("")

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    water_lvl_pin = 14  # ultrasonic rangerfinder @ D3
    grovepi.pinMode(water_lvl_pin, "INPUT")
    while True:
        substrate_moisture_lvl = (max(500.0, min(grovepi.analogRead(14), 730.0))-500.0)/2.3
        client.publish("wangsiya/water_levelRead", substrate_moisture_lvl)
        time.sleep(2)
