#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 17:14:48 2016

@author: rorix
"""

import RPi.GPIO as GPIO
import glob, os, random, time
import pygame.mixer
from mutagen.mp3 import MP3

# initialize GPIO ports
PIR_pin = 15
b1_pin = 11
b2_pin = 13
led_pin = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(b1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set as a pull up resistor
GPIO.setup(b2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)
# this setup of the buttons means we connect the GPIO pins connected to b1 and
# b2 to the switch, which is then connected to ground

class ShutDown(Exception): pass

def stateSetup():
    global active
    global playing
    active = 0
    playing = lambda: False
    print('Initializing system')
    print('Currently not tracking motion')

def stateToggle(channel):
    global active
    if active==1:
        active = 0
        print('Motion detection deactivated')
    elif active==0:
        print('Activating motion sensor in 10s')
        for i in range(0,10):
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(0.5)
        active = 1
        GPIO.output(led_pin, GPIO.HIGH)
        print('Motion detection activated')
        
def shutdown(channel):
    print('Shutting down')
    time.sleep(0.5)
    GPIO.output(led_pin, GPIO.LOW)
    pygame.mixer.music.stop()
    raise ShutDown
        
# define fisher yates playlist generator
def playlist_gen():
    playlist = range(n)
    random.shuffle(playlist)
    return playlist
    
def motionSensor(channel):
    if GPIO.input(PIR_pin) and active==1 and playing()==False:
        global counter
        global playlist
        global playing
        
        curr_pos = playlist[counter % n]
        name = tracklist[curr_pos]
        # sleep for 5 secondes before starting playback
        time.sleep(5)
        # define timed variable such that
        # playback does not get interrupted
        now = time.time()
        playing = lambda: time.time() < now + tracklength[curr_pos]
        # load and play track
        pygame.mixer.music.load(name + '.mp3')
        pygame.mixer.music.play()
        # update counter
        counter +=1
        # if all tracks have been played once then create new playlist
        if counter % n == 0:
            playlist = playlist_gen()
        

# initialize pygame mixer
pygame.mixer.init(44100,-16,2,4096)
pygame.mixer.music.set_volume(1.0)

# get list of available mp3 files and their length
#os.path.expanduser('~')
#os.chdir(os.path.expanduser('~/Downloads/FF-intro'))
tracklist = [file for file in glob.glob('*.mp3')]
tracklength = [int(MP3(f).info.length) for f in tracklist]
n = len(tracklist)

# initialize playlist
playlist = playlist_gen()

# initialize replay counter
counter = 0
# initialize playing variable

stateSetup()

GPIO.add_event_detect(PIR_pin, GPIO.BOTH, callback=motionSensor, bouncetime=150)
GPIO.add_event_detect(b1_pin, GPIO.LOW, callback=stateToggle, bouncetime=150)
GPIO.add_event_detect(b2_pin, GPIO.LOW, callback=shutdown, bouncetime=150)

try:
    while True:
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
except ShutDown:
    GPIO.cleanup()
finally:
    GPIO.cleanup()