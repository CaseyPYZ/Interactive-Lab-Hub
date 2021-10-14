# Chatterboxes
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Additional Parts

As mentioned during the class, we ordered additional mini microphone for Lab 3. Also, a new part that has finally arrived is encoder! Please remember to pick them up from the TA.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2021
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using a USB microphone, and the speaker on your webcamera. (Originally we intended to use the microphone on the web camera, but it does not seem to work on Linux.) In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

One thing you might need to pay attention to is the audio input setting of Pi. Since you are plugging the USB cable of your webcam to your Pi at the same time to act as speaker, the default input might be set to the webcam microphone, which will not be working for recording.

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

Bonus Activity:

If you are really excited about Speech to Text, you can try out [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) and [voice2json](http://voice2json.org/install.html)
There is an included [dspeech](./dspeech) demo  on the Pi. If you're interested in trying it out, we suggest you create a seperarate virutal environment for it . Create a new Python virtual environment by typing the following commands.

```
pi@ixe00:~ $ virtualenv dspeechexercise
pi@ixe00:~ $ source dspeechexercise/bin/activate
(dspeechexercise) pi@ixe00:~ $ 
```

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

<img src="./IDD_Lab3_sketch.jpeg">

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

### Acting out the dialogue

>Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

[VIDEO LINK](https://youtu.be/duMpP3hxm-g)

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*



### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...

* One thing I noticed in part 1 is that the wording of the conversation needs to be more carefully designed, and shouldn't leave too much vague space for interpretation. Or else the user might interpret meanings differently, and go on a interation path that's not originally in the picture.

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

* I think touch would work well in my design. My device "the debug duck" is meant to stay idle for most of the time, and only be active when the user talks to it. A "hello Siri" type of speech trigger is cool, but touch-based activation would be more stable and robust.

3. Make a new storyboard, diagram and/or script based on these reflections.


## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

*Include videos or screencaptures of both the system and the controller.*

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

#### **What worked well**
1. The participant loved actually having and seeing a duck on their desk, even though it's still a prototype. But given their feedback, it's a completely different experience from looking at a image of a duck on the screen. This made me realize how important the presence of a touchable object is to the embodiment of the interaction, even just a prototype of the actual device.

2. **An important feedback from participants in part 1 is that sometimes it's hard to tell if the duck is activated problem-free when it fully relied on voice.** Now with the device activated through a switch instead of purely voice, activation status is more clear. 

* **NOTE: CLEARER ACTIVATION**

#### **What did not work well**

1. The system still trumbled a bit on **when to deciced a stop in the user's speech is detected**. While speaking, people naturally make pauses, especially when they are walking themselves through a complicated coding question. Sometimes when it's a long pause, the system falsely determin a stop of speech and begins responding. I thought about using a **check sentence** such as "Is that all?" to proactively check for a end of conversation, but did not like how it breaks the naturalness of the speech interaction.

* **NOTE: END OF SPEECH DETERMINATION** 

2. Originally, the system is designed to have a "search assistant" feature, where the duck will ask the user if they'd like the duck to look for answers on Google/other search engine/Stackoverflow/etc. after hearing the question. In part 1, I found out that this interaction flow doesn't always go smoothly. **Users do not feel like this is adding value for them.** Looking up answers online itself is a easy task to carry out, having to verbally asking a program/device to do that for you is not making it easier, and perhaps even harder.

* **NOTE: ONLY ADD WHAT'S TAKING OFF BURDENS / ADDING VALUES FOR THE USER**

### What worked well about the controller and what didn't?

* This version of the device does not involve a remote/online controller, other than a simple "on/off" switch.
* However, given that there's a "note-archive" aspect to the design, I think the system is only complete with a software interface that allows storage, view and edit of notes, which should be in both audio and speech-to-text transcripted text form. (Or should this be by the user's choice?)

* **NOTE: SOFTWARE INTERFACE?** 


### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?


* Something that's really important for a autonomous system is that it needs to be well-designed for all states, idle, activated, before/after interaction. Even for a simple system like the Debug Ducky, its states need to be carefully planned. What should be its default status (always listening? only when mannually turned on?), how should a user switch it between states, are all meaningful decisions to make.

* Presence of a autonomous device/system in the user's living/working/studying environment has psycological/emotional impacts, which also needs attentions.

* Experiences a autonomous systems creates largely depends on its robustness. During user tests, whenever the prototype reated differently from the user's expectation, (for example, when it's not activated successfully / thought the speech input has ended when it hasn't), the interative experience is broken. **Robustness is crucial yet hard to achive.**


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

<br>
To me, speech audio generated by the users are valuable data to collect in this process. The key idea behind the Debug Ducky is that people often figure out problems by processing it again, and speaking out loud the thingking process in their mind is very helpful in this sense. The Debug Duck is like a coding buddy that's always ready to code in pairs with you or just listen to your bugs.

Therefore, what people say, when they choose to say it, the effectiveness of speaking out your coding problems to a rubber duck, are all valuable information we can study from speech data inputed to this system.
