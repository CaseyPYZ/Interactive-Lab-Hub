import time
import threading

import board
import busio
import paho.mqtt.client as mqtt
import uuid
import sparkfun_qwiicjoystick
from adafruit_servokit import ServoKit


# Set up MQTT connection
def set_mqtt_connection():
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')

    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)
    
    return client

class ServoThread(threading.Thread):
    def __init__(self, name, channel_num, port1, port2, mqtt_client, mqtt_topic):
        threading.Thread.__init__(self, name=name, daemon=False)
        self.name = name
        self.kit = ServoKit(channels=channel_num)
        self.servo1 = self.kit.servo[port1]
        self.servo2 = self.kit.servo[port2]
        self.servo1.set_pulse_width_range(500, 2500)
        self.servo2.set_pulse_width_range(500, 2500)
        self.mqtt_client = mqtt_client
        self.read_topic = mqtt_topic

    def on_message(self, client, userdata, msg):
        msg = msg.payload.decode('UTF-8')
        print("Servo reads> ", msg)
        if msg == 'U':
            self.servo1.angle = 0
            self.servo2.angle = 0
            time.sleep(0.5)
        elif msg == 'D':
            self.servo1.angle = 90
            self.servo2.angle = 90
            time.sleep(0.5)

    def run(self):
        # Subscirbe to topic
        self.mqtt_client.subscribe(self.read_topic)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.loop_forever()



class JoystickThread(threading.Thread):
    def __init__(self, name, mqtt_client, mqtt_topic):
        threading.Thread.__init__(self, name=name, daemon=False)
        self.name = name
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.joystick = sparkfun_qwiicjoystick.Sparkfun_QwiicJoystick(self.i2c)
        self.mqtt_client = mqtt_client
        self.write_topic = mqtt_topic
    
    def run(self):
        # Check if connected
        if self.joystick.connected:
            print("Joystick connected.")
        else:
            print("Joystick does not appear to be connected. Please check wiring.")
            sys.exit()

        print("Joystick Version: " + self.joystick.version)
        print("Type Ctrl-C to exit program.")

        try:
            while True:
                x = self.joystick.horizontal
                y = self.joystick.vertical
                b = self.joystick.button

                # print horizontal direction
                if x > 575:
                    print("Jstick> L")
                    val = "L"
                    self.mqtt_client.publish(self.write_topic, val)
                if x < 450:
                    print("Jstick> R")
                    val = "R"
                    self.mqtt_client.publish(self.write_topic, val)

                # print vertical direction
                if y > 575:
                    print("Jstick> U")
                    val = "U"
                    self.mqtt_client.publish(self.write_topic, val)
                if y < 450:
                    print("Jstick> D")
                    val = "D"
                    self.mqtt_client.publish(self.write_topic, val)

                # print button state
                if b == 0:
                    print("Button")
                    val = "Btn"
                    self.mqtt_client.publish(self.write_topic, val)

                # sleep a bit to slow down messages
                time.sleep(0.5)

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    # Servo Controller vars
    SERVO_CHANNEL_NUM = 16
    SERVO_PORT_1 = 0
    SERVO_PORT_2 = 15

    # MQTT Topics
    READ_FROM = 'B'
    WRITE_TO = 'A'
    READ_TOPIC = 'IDD/kcp/talking_ps/' + READ_FROM
    WRITE_TOPIC = 'IDD/kcp/talking_ps/' + WRITE_TO

    try:
        mqtt_client = set_mqtt_connection()

        # Joystick Thread
        joystick_thread = JoystickThread('jstick', mqtt_client, WRITE_TOPIC)
        joystick_thread.start()

        # Servo Thread
        servo_thread = ServoThread('servo', SERVO_CHANNEL_NUM, SERVO_PORT_1, SERVO_PORT_2, mqtt_client, READ_TOPIC)
        servo_thread.start()

    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nExiting")
        sys.exit(0)