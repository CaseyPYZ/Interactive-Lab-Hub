import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import sys

import paho.mqtt.client as mqtt
import uuid

# Set up MQTT connection
def set_mqtt_connection():
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set()
    client.username_pw_set('idd', 'device@theFarm')

    client.connect(
        'farlab.infosci.cornell.edu',
        port=8883)
    
    return client


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


    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    channel = AnalogIn(mcp, MCP.P0)

    VOLT_THRESHOLD = 0.1
    

    try:
        mqtt_client = set_mqtt_connection()

        while(True):
            # print('Raw ADC Value: ', channel.value)
            # print('ADC Voltage: ' + str(channel.voltage) + 'V')
            
            volt = channel.voltage
            print('ADC Voltage: ' + str(volt) + 'V')
            val = "F"

            if volt < 0.5 - VOLT_THRESHOLD:
                val = "T"

            mqtt_client.publish(WRITE_TOPIC, val)
            print("Written to MQTT client> " + val)

            time.sleep(0.5)
            



    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nExiting")
        sys.exit(0)