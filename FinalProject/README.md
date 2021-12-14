
# Project Handover 

## Idea Formation

### Idea Generation

Our original idea was initially inspired by this clip from a Netflix show *Space Force*. 

https://user-images.githubusercontent.com/42874337/141866447-08171305-cf33-4ae6-b19a-00f89f40d4b0.mp4

During the age of pandemic, our device was then inspired by the increasing prevalence of virtual meetings. In the recent years, more and more first encounters between people occurred through a video conference or zoom meeting instead of actual presenting in a physical space. A remote handshaking device would be a art-oriented, but symbolic project that reflects the society's needs. As the technical details being set, this could also have potential practical usage as products that would allow people to perform delicate but dangerous tasks remotely like defusing a bomb, or operate a surgery if physical present is not avaliable. 

### Sketch

Here is our sketch of the device:

![HandOver Sketch](https://user-images.githubusercontent.com/37056925/141871861-85184969-8062-4a41-a4cd-aa189144ba8d.jpeg)

### Technical detail Set-Up

After completing the device design, we started with testing some basic technical details to ensure the idea is achivable, here's the video record of our first attempt to communicate over Pi and control motors from the other side using joysticks over MQTT server. This set up the basic ideas of how are we going to remotely control the hand. 

https://user-images.githubusercontent.com/37056925/141871832-587517cf-29a8-4276-8d40-63e9abbc3f79.mp4

Here was our project plan that we set up before the start of actual project. We have basically followed the workflow as we planned, but make slight changes to the way we achieve all the technical details and also improvised a little on the physical prototyping. 

[Project Plan](https://github.com/CaseyPYZ/Interactive-Lab-Hub/blob/Fall2021/FinalProject/IDDFinalProjectPlan.docx)

## Procedure

### Parts Used

* Raspberry Pi
* MCP3008 ADC Module
* Servo Motor(s): SG90 9g


### Physical Prototyping

#### 1. Hand part (controlled)

(Details about hand model)
We have 3-D printed the whole hand, with different materials. We started with solid PCA materials for all parts at the beginning, as shwon on the picture below:

![image](https://user-images.githubusercontent.com/42874337/145881453-a77b494e-2c8b-4c88-9379-402507bb385e.png)

However, the problem was the hand was not able to move since the PCA material is not flexible enough. We have then reprinted all the joints using another flexible material, which matains a certain shape while able to bend as we expected: 

![image](https://user-images.githubusercontent.com/42874337/145881701-0b2c480a-a4b8-4db0-bff3-1fedcea1022f.png)

We have also printed a wrist part using the same materials as joints to allow slight wrist movement when shaking hands.

Here's the final hand model that we developed, that controlled by a string for each finger, and all fingers can move seperately. 

https://user-images.githubusercontent.com/42874337/145883689-247aa64c-254c-4f4c-9deb-1bc4932a7b6e.mp4


#### 2. Gloves part (controller)

In order to accurately detect the hand gesture made from the input end, we decide to use flexisensors (bending sensor) that would be able to detect the change of resistance within a circuit when bended. 

This is how we connect a flexisensor to raspberry pi (through a breadboard).

![image](https://user-images.githubusercontent.com/42874337/145885891-a060bdc2-a079-4911-a65e-e0aa2aa3ee88.png)

![image](https://user-images.githubusercontent.com/42874337/145886024-e8167439-db86-4552-afd7-0a185f537f02.png)

After making sure of the sensor's ability of outputing continuous data, we extend it using wires and attached 5 flexisensors to a glove on the palm side. 

![image](https://user-images.githubusercontent.com/42874337/145886390-ce40f184-7539-409c-90fa-a35e2df7a4db.png)

We found the tape is not strong enough to hole the sensors on the glove and makes it too fragile, so we decided to solder the sensors to the wires directly. 

![image](https://user-images.githubusercontent.com/42874337/145887345-5ebd45c1-0a89-449f-ae86-ff95b42f0b1a.png)
![image](https://user-images.githubusercontent.com/42874337/145887373-9fec48b8-57c4-474a-b594-debecb9b85b7.png)

#### 3. Final Device

After setting up the glove, our pi was then able to read in data from flexisensors on it and then send signals to the other pi that controls the hand model remotely over MQTT server (technical details see programming implementaton section). In order to map the finger movement from the glove to the hand, we have utilized 5 servo motors to control the strings of the hand model. Each motor is attached to one finger, which coresponds to the signal sent by hand movement in the glove. 

![image](https://user-images.githubusercontent.com/42874337/145892997-01a97665-bdd2-46f8-9255-414a09e976b5.png)

We have also attached the wrist part of the hand model to a monitor stand, which allows a screen to be placed on top for video while hand at the bottom for handshake. 

https://user-images.githubusercontent.com/42874337/145891914-09b46474-12a8-48d4-9788-9f4e4136ffe1.mp4

#### 4. Designer Test

Here's the video record of the first attempt of the designer's test:

https://user-images.githubusercontent.com/42874337/145894466-4d5b5b00-47e2-4226-8628-a017a9ec071a.mp4


### Programming Implementation


#### **Reading Flex Sensors: Analog Input for Raspberry Pi**

In this project, we are using flex sensors which give analog values as our input. Since raspberry Pis do not inheritly have analog inputs, adding analog inputs from sensors to Raspberry Pi is one of the major technical focal points we had for this project.

**0 - Threading**

In this project, we are working with 5 flex sensors, each controlling their own corresponding servo motor. In order for these 5 channels of data transmission to work smoothly without interfering with each other, we used threading in our program.

Each flex sensor and servo motor are on their own thread. One thing to notice is that MQTT does not support multi-threading on a single client, so we established a separate MQTT connect (client) for each thread. 

Each pair of flex sensor and servo motor communicate through their own MQTT topic named after the servo motor's pin number.

**1 - Setting Up ADC Module**

In order for our raspberry pi to read analog sensor values, we will need a Analog-to-Digital-Converter (ADC) Module.

We chose to use *MCP3008 8-channel ADC module*, because it is well-compatible with CircuitPython microcontroller boards and computer that has GPIO and Python, with the help of **adafruit_mcp3xxx.mcp3008** module.

We followed the steps in this very helpful adafruit tutorial by Kattni Rembor:

>**[MCP3008 - 8-Channel 10-Bit ADC With SPI Interface](https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython)**

**1.1 Wiring**

For circuit wiring, the MCP3008 ADC modules needs to be connected to the Pi as shown here:

![MCP3008 circuit](./img/adafruit_products_raspi_MCP3008_spi_bb.png 'MCP3008 Circuit')

> * MCP3008 CLK to Pi SCLK 
> * MCP3008 DOUT to Pi MISO
> * MCP3008 DIN to Pi MOSI
> * MCP3008 CS to Pi D5
> * MCP3008 VDD to Pi 3.3V
> * MCP3008 VREF to Pi 3.3V
> * MCP3008 AGND to Pi GND
> * MCP3008 DGND to Pi GND
> * MCP3008 CH0 to Potentiometer middle pin
> * Potentiometer left pin to Pi GND
> * Potentiometer right pin to Pi 3.3V

**1.2 Programming Setup**

Using modules *busio*, *digitalio*, *board* and *adafruit_mcp3xxx.mcp3008*, we are able to establish channels corresponding to the 8 channels of MCP3008, and read the raw ADC values and voltages from them.

Following is a piece of sample setup code.

```python
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)

### Now you can read inputs through the following properties
# voltage: the voltage from the ADC pin as a floating point value 
# value  : the value of an ADC pin as an integer.

print('Raw ADC Value: ', channel.value)
print('ADC Voltage: ' + str(channel.voltage) + 'V')

```

**2 - Flex Sensors**

We choose to use flex sensors to detect finger bending. Flex sensors are basically resistors that change value based on how much their flexed. If they're unflexed, the resistance is about ~25KΩ. When flexed all the way the resistance rises to ~100KΩ. 

They are very similar to Force Sensitive Resistors (FSRs) which are also value-changing resistors, so we followed the following adafruit tutorial on FSRs by lady ada to set up our flex sensors.

>**[Force Sensitive Resistor (FSR)](https://learn.adafruit.com/force-sensitive-resistor-fsr/using-an-fsr)**


**2.1 Wiring**

![Flex Sensor Wiring](./img/force___flex_fsrpulldowndia.png 'Flex Sensor Wiring')

The flex sensors are wired as follows just like many other sensors. Wire the sensor up one pin to a 3.3V pin of your RPI and the other pin to a ground pin, in serial with a resistor of your choice. We used a **6k8Ω** resistor in our circuit.

The extra resistor used here is to put a capita on the voltage distributed to the flex sensor. It's sometimes used to protect the sensor itself or the controller board. In our case, since we are using a 3.3V power from the RPi, the extra resistor is not necessary protection-wise.

Value of the extra resistor can vary depending on how wide you want the voltage range on the sensor to be. In other words, it controls the **sensitivity** of your sensor. This will have an affect on how you map the values on software level.

Use another wire to connect this subcircuit to a data pin. The graph is demostrating the circuit with an Arduino board, **in our case, the data pin would be one of the 8 channels of our MCP3008 module**.

The flex sensor is non-polarized, so the two pins can be connected in either direction.

**2.2 Programming**

With our circuit setup and choice of resistance, the values our flex sensors give approximately fall in the range of **[0.2V, 0.8V]**.

For simplicity, we have the flex sensor control system set to a binary state. When the voltage read from the sensor is above a set value (meaning that sensor is being bent), we send a "T" message to the MQTT server for the corresponding servo motor, which will then turn to an 'activated' mode (turning 180 degree) upon reading the message. Similarly, when the voltage value is delow a set value, we send a "F" message to the MQTT server for the corresponding servo motor, which will then turn to a 'deactivated' mode (turning 180 degree) upon reading the message.

Note that on idle state, the voltage values read from the sensor are not still, but rather shakea a little in a certain range. In our case, it's 0.5V ~ 0.7V. Thus, we set a threshold of 0.2V to separate the ON and OFF value ranges for the system.

```python
if volt > THRESHOLDS[self.s_pin] + VOLT_THRESHOLD:
    val = "T"
```

This way, the flex sensors serve pretty well as switches for their corresponding servo motors.


#### **Servo Motor Control**





## User Test

After constructing the initial physical prototype we tested the concept with a handful of peers. We let our testers participate at both ends of the interaction (both shaking the hand and wearing the glove which controls the hand) and noted down any bugs in our implementation and our user feedback. From our testing we noticed 3 main points of improvement

1. The sensors we attached to the glove were not bending along with the movement of the thumb (as it is normally angled differently from other fingers). 
2. Performing a handshake without establishing eye contact was somewhat jarring .
3. Holding and shaking the hand felt unnatural as the device was not designed to support wrist movements.

## Improvement

Upon receiving feedback from testing we iterated on the device to improve its functionality. 

First we stripped down the sensor glove and reattached the flex sensors while a participant was wearing it to properly align the sensors with finger movements. We also created a “wrist” model in CAD and 3D printed a hollow version out of soft material; the soft material allows the hand to have some flex and motion along the wrist joint after being mounted.

![Fresh Printed Wrist](https://github.com/CaseyPYZ/Interactive-Lab-Hub/blob/Fall2021/FinalProject/img/IMG_1958.JPG =400x300)

Lastly, we decided to integrate a display into our device and broadcast Zoom video through it to give the user another participant to look at while interacting with the device.


## Presentation & Impact

In our demo, we presented the device in two different portions; a read side where users could shake the artificial hand, and a write side where users could send signals to move the hand. The read side was created by combining our artificial hand attached to servo motors with a monitor stand and a display. The stand could be adjusted so that the display featuring another participant’s face could be eye-level and that the hand was closer to the user’s waist.

The write portion consisted of flex sensors soldered and glued onto a glove, which were connected to a circuit board sending signals to the pi. The sensor glove was designed so that anyone who put the glove on correctly (on their right hand with sensors facing down) could operate the hand remotely, as the hand is meant to copy their finger movements.

![image](https://user-images.githubusercontent.com/42874337/145887507-4b26d295-4672-4f2b-bc13-8cb9526e797f.png)

On the presentation day, we had a lot of wires and electrical components visible to the user for the purpose of explaining our implementation and easily accessing parts in case of repairs. However, due this we noticed some apprehension in users physically touching and interacting with both read and write portions of the device. A more polished version would have the hardware hidden away so the users would be comfortable with interacting with it.

![image](https://user-images.githubusercontent.com/42874337/145887526-f954748b-8515-42ed-be8f-dbb3c12b127d.png)

We have also presented the project during the Open Studio Day at Maker Lab, we have received many practical advices from visitors and peers like:

1. Back string to control open movement of the fingers
2. Scale the movement and map it to the hand model more accurately
3. Put the flexisensors on the back of the gloves

We are also the only project throughout the whole open studio that being posted by the official Cornell Tech Instagram!

