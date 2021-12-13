
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


### Programming Implementation

## User Test

After constructing the initial physical prototype we tested the concept with a handful of peers. We let our testers participate at both ends of the interaction (both shaking the hand and wearing the glove which controls the hand) and noted down any bugs in our implementation and our user feedback. From our testing we noticed that the sensors we attached to the glove were not bending along with the movement of the thumb (as it is normally angled differently from other fingers). We also received feedback that performing a handshake without establishing eye contact was somewhat jarring, and that moving the hand felt unnatural as the device was not designed to support wrist movements.

## Improvement

Upon receiving feedback from testing we iterated on the device to improve its functionality. We stripped down the sensor glove and reattached the flex sensors while a participant was wearing it to properly align the sensors with finger movements. We also created a “wrist” model in CAD and 3D printed a hollow version out of soft material; the soft material allows the hand to have some flex along the wrist joint after being mounted. Lastly, we decided to integrate a display into our device and broadcast Zoom video through it to give the user another participant to look at while interacting with our device.


## Presentation & Impact

In our demo, we presented the device in two different portions; a read side where users could shake the artificial hand, and a write side where users could send signals to move the hand. The read side was created by combining our artificial hand attached to servo motors with a monitor stand and a display. The stand could be adjusted so that the display featuring another participant’s face could be eye-level and that the hand was closer to the user’s waist.

The write portion consisted of flex sensors soldered and glued onto a glove, which were connected to a circuit board sending signals to the pi. The sensor glove was designed so that anyone who put the glove on correctly (on their right hand with sensors facing down) could operate the hand remotely, as the hand is meant to copy their finger movements.

![image](https://user-images.githubusercontent.com/42874337/145887507-4b26d295-4672-4f2b-bc13-8cb9526e797f.png)

On the presentation day, we had a lot of wires and electrical components visible to the user for the purpose of explaining our implementation and easily accessing parts in case of repairs. However, due this we noticed some apprehension in users physically touching and interacting with both read and write portions of the device. A more polished version would have the hardware hidden away so the users would be comfortable with interacting with it.

![image](https://user-images.githubusercontent.com/42874337/145887526-f954748b-8515-42ed-be8f-dbb3c12b127d.png)


## Reflection

