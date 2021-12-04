import sys
import time
import threading
import uuid

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


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
    def __init__(self, name, servo, mqtt_client, mqtt_topic):
        threading.Thread.__init__(self, name=name, daemon=False)
        self.name = name
        # self.pin = servo_pin
        # # self.GPIO = gpio
        # # self.GPIO.setup(self.pin, self.GPIO.OUT)
        # # self.servo = self.GPIO.PWM(self.pin, 50)
        # GPIO.setup(self.pin, GPIO.OUT)

        self.servo = servo
        self.mqtt_client = mqtt_client
        self.read_topic = mqtt_topic

    def on_message(self, client, userdata, msg):
        msg = msg.payload.decode('UTF-8')
        print("Servo reads> ", msg)
        if msg == 'T':
            duty = 2
            while duty <= 17:
                self.servo.ChangeDutyCycle(duty)
                time.sleep(0.1)
                duty = duty + 1
            # self.servo.ChangeDutyCycle(16)
            # time.sleep(0.5)
        elif msg == 'F':
            self.servo.ChangeDutyCycle(0)
            # time.sleep(0.5)

    def run(self):
        self.servo.start(0)
        print("Servo started")
        # Subscirbe to topic
        self.mqtt_client.subscribe(self.read_topic)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.loop_forever()



# servo.start(0)
# print ("Waiting for 1 second")
# time.sleep(1)

# print ("Rotating at intervals of 12 degrees")
# duty = 2
# while duty <= 17:
#     servo.ChangeDutyCycle(duty)
#     time.sleep(1)
#     duty = duty + 1

# print ("Turning back to 0 degrees")
# servo.ChangeDutyCycle(2)
# time.sleep(1)
# servo.ChangeDutyCycle(0)

# servo.stop()
# GPIO.cleanup()
# print ("Everything's cleaned up")



if __name__ == '__main__':
    # Servo Controller vars
    SERVO_PIN = 11

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo = GPIO.PWM(SERVO_PIN, 50)

    
    # MQTT Topics
    READ_FROM = 'A'
    WRITE_TO = 'A'
    READ_TOPIC = 'IDD/kcp/talking_ps/' + READ_FROM
    WRITE_TOPIC = 'IDD/kcp/talking_ps/' + WRITE_TO


    # spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # cs = digitalio.DigitalInOut(board.D5)
    # mcp = MCP.MCP3008(spi, cs)
    # channel = AnalogIn(mcp, MCP.P0)
    

    try:
        mqtt_client = set_mqtt_connection()

        servo_thread = ServoThread('servo', servo, mqtt_client, READ_TOPIC)
        servo_thread.start()

        


    except (KeyboardInterrupt, SystemExit) as exErr:
        servo.stop()
        GPIO.cleanup()
        print ("Everything's cleaned up")

        print("\nExiting")
        sys.exit(0)