# Seagull Scaring V2
A seagull scaring program with GUI written in Python.
By Gabriel Alonso-Holt.

The days of having me run around scaring seagulls manually are over! With Seagull Scaring, you can just start the program, choose a time to scare seagulls for, and relax as the seagulls fly away when you want.

**Before you proceed, sound effects are not included!**

Recommended settings: 2700 seconds (timer), 60 seconds (min time), 300 seconds (max time), seagull (sound).

### About this project
Seagull Scaring was created to stop the biggest problem plaguing my school since I can’t remember when. 
It has been tested to have a 98% success rate against seagulls (or shall I say gulls) of all shapes and sizes! 
Seagull Scaring V2 is a user-friendly GUI interface for Seagull Scaring 1.4 written using the CustomTkinter library. 
The recommended settings are meant to be used during 1 lunchtime.

### Install instructions
1. Unzip the program folder.
2. Set up the virtual environment and install dependencies. (see below)
3. Copy a `media.zip` to the program folder, run `main.pyw`, click "about" and then click "extract gull effects".

### Installing dependencies
1. Run this command to create a virtual environment: `python -m venv .venv`
2. Activate the environment: `.venv\Scripts\activate.bat`
3. Install dependencies: `pip install -r requirements.txt`
4. Run program: `python main.pyw`

### Config file documentation
In the program directory, there is a file called `ssv2cfg.ini`.

You may edit this file as you desire.

**All settings must go in the [main] section.**

Valid settings: 

`scaring_time (int)`: How long to run the program for.

`min_time (int)`: Minimum time to wait.

`max_time (int)`: Maximum time to wait.

`default_volume (int)`: Default volume from 0-100.

`default_sound (str)`: Seagull sound to use. Valid options: seagull, sad seagull, angry seagull, confused seagull, disgust seagull, robot seagull, alarm seagull, Seagull 2, sea gull.

`autostart (str)`: Enable/disable autostart feature. Valid options: yes/no.

`autostart_delay (int)`: Delay seconds for the autostart feature. Not working as of 17/02/2025.

### Sending announcements
To send an announcement, you will need an `alarm_seagull.wav` either from Gabriel's Seagull Sound Pack or your own choosing.
Click "send announcement" in the program window and a text box will appear for you to enter your message.
Once you click OK, the alarm seagull sound effect will play twice, then a TTS voice will say "This is a Seagull Wars public service announcement", read out your message, and play the alarm seagull sound twice again.