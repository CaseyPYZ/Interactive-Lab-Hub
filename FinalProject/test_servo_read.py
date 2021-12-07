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

# Degree  | Duty cycle percentage
# -90     | 5
# neutral | 7.5
# +90     | 10

class ServoThread(threading.Thread):
    def __init__(self, name, gpio, servo_pin, mqtt_client, mqtt_topic):
        threading.Thread.__init__(self, name=name, daemon=False)
        self.name = name
        self.pin = servo_pin
        self.GPIO = gpio
        self.GPIO.setup(self.pin, self.GPIO.OUT) # setup GPIO PIN
        self.servo = self.GPIO.PWM(self.pin, 50)

        # self.servo = servo
        self.bent = False
        self.mqtt_client = mqtt_client
        self.read_topic = mqtt_topic

    def set_angle(self, angle):
        duty = angle / 18 + 2
        print("duty> ", duty)
        self.GPIO.output(self.pin, True)
        self.servo.ChangeDutyCycle(duty)
        time.sleep(1)
        self.GPIO.output(self.pin, False)
        self.servo.ChangeDutyCycle(0)
        
    def on_message(self, client, userdata, msg):
        msg = msg.payload.decode('UTF-8')
        print("Servo reads> ", msg, "servo.bent> ", self.bent)
        if msg == 'T':
            # Bend finger
            if self.bent == False:
                self.set_angle(180)
                self.bent = True
        elif msg == 'F':
            # Unbend finger
            if self.bent == True:
                self.set_angle(0)
                self.bent = False

    def run(self):
        self.servo.start(0)
        print("Servo started")
        # Subscirbe to topic
        self.mqtt_client.subscribe(self.read_topic)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.loop_forever()


# Servo Controller vars
SERVO_NUM = 5
SERVO_PINS = [11, 15, 29, 31, 33]
servo_threads = []


if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)
    
    # MQTT Topics
    READ_FROM = 'A'
    WRITE_TO = 'A'
    READ_TOPIC = 'IDD/kcp/talking_ps/' + READ_FROM + '/'
    WRITE_TOPIC = 'IDD/kcp/talking_ps/' + WRITE_TO + '/'
    

    try:
        for i in range(SERVO_NUM):
            mqtt_client = set_mqtt_connection()
            servo_thread = ServoThread('servo', GPIO, SERVO_PINS[i], mqtt_client, READ_TOPIC+str(i))
            servo_threads.append(servo_thread)

        for i in range(SERVO_NUM):
            servo_threads[i].start()
            



    except (KeyboardInterrupt, SystemExit) as exErr:
        servo.stop()
        GPIO.cleanup()
        print ("Everything's cleaned up")

        print("\nExiting")
        sys.exit(0)