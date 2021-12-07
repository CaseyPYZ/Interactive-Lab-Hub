import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import sys
import threading

import paho.mqtt.client as mqtt
import uuid


SERVO_PINS = [11, 15, 29, 31, 33]

MCP_PIN_DICT = {
    11: MCP.P0,
    15: MCP.P1,
    29: MCP.P2,
    31: MCP.P3,
    33: MCP.P4
}

# Set up MQTT connection
def set_mqtt_connection():
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')

    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)
    
    return client


class FlexSensorThread(threading.Thread):
    def __init__(self, name, mcp, servo_pin, mqtt_client, mqtt_topic):
        threading.Thread.__init__(self, name=name, daemon=False)
        self.name = name
        self.s_pin = servo_pin
        self.mcp = mcp
        # self.servo = self.GPIO.PWM(self.pin, 50)
        self.channel = AnalogIn(self.mcp, MCP_PIN_DICT[self.s_pin])
        # self.servo = servo
        # self.bent = False
        self.mqtt_client = mqtt_client
        self.write_topic = mqtt_topic

    def run(self):
        print(self.name + " thread started")
        while(True):
            volt = self.channel.voltage
            print(self.name + ' ADC Voltage: ' + str(volt) + 'V')
            val = "F"
            if volt > 0.5 + VOLT_THRESHOLD:
                val = "T"

            self.mqtt_client.publish(self.write_topic, val)
            print(self.name + " written> " + val)

            time.sleep(0.5)


FSENSOR_NUM = 5
fsensor_threads = []

VOLT_THRESHOLD = 0.2

if __name__ == '__main__':

    # MQTT Topics
    READ_FROM = 'A'
    WRITE_TO = 'A'
    READ_TOPIC = 'IDD/kcp/talking_ps/' + READ_FROM + '/'
    WRITE_TOPIC = 'IDD/kcp/talking_ps/' + WRITE_TO + '/'


    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    # channel = AnalogIn(mcp, MCP.P0)

    
    try:
        for i in range(FSENSOR_NUM):
            mqtt_client = set_mqtt_connection()
            fsensor_thread = FlexSensorThread('fsensor'+str(i), mcp, SERVO_PINS[i], mqtt_client, WRITE_TOPIC+str(i))
            fsensor_threads.append(fsensor_thread)

        for i in range(FSENSOR_NUM):
            fsensor_threads[i].start()



    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nExiting")
        sys.exit(0)