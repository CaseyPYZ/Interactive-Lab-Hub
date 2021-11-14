import time
import board
import busio

import paho.mqtt.client as mqtt
import uuid

import qwiic
import qwiic_joystick
import sparkfun_qwiicjoystick

# Set up MQTT connection
def set_mqtt_connection():
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')

    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)
    
    return client

def runJoystick(mqtt_client):
 
    mqtt_topic = 'IDD/kcp/joystick_val'

    i2c = busio.I2C(board.SCL, board.SDA)

    # Set up sensor
    # Create joystick object
    joystick = sparkfun_qwiicjoystick.Sparkfun_QwiicJoystick(i2c)
    # joystick = sparkfun_qwiicjoystick.Sparkfun_QwiicJoystick(i2c, other_addr)

    # Check if connected
    if joystick.connected:
        print("Joystick connected.")
    else:
        print("Joystick does not appear to be connected. Please check wiring.")
        sys.exit()

    print("Joystick Version: " + joystick.version)
    print("Type Ctrl-C to exit program.")

    try:
        while True:
            x = joystick.horizontal
            y = joystick.vertical
            b = joystick.button

            # print horizontal direction
            if x > 575:
                print("L")
                val = "L"
                mqtt_client.publish(mqtt_topic, val)
            if x < 450:
                print("R")
                val = "R"
                mqtt_client.publish(mqtt_topic, val)

            # print vertical direction
            if y > 575:
                print("U")
                val = "U"
                mqtt_client.publish(mqtt_topic, val)
            if y < 450:
                print("D")
                val = "D"
                mqtt_client.publish(mqtt_topic, val)

            # print button state
            if b == 0:
                print("Button")
                val = "Btn"
                mqtt_client.publish(mqtt_topic, val)

            # sleep a bit to slow down messages
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        mqtt_client = set_mqtt_connection()
        runJoystick(mqtt_client)

    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)