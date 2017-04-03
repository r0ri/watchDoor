#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 18:17:29 2016

@author: rorix
"""

import RPi.GPIO as GPIO
import glob, os, random, time
import vlc
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

def stateSetup():
    global active
    active = 0
    print('Initializing system')
    print('Currently not tracking motion')

def stateToggle():
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

# define fisher yates playlist generator
def playlist_gen():
    global playlist
    playlist = range(n)
    random.shuffle(playlist)
        
def watchdoor():
    global counter
    global playing
    while True:
        if GPIO.input(PIR_pin)==1 and playing()==False and active==1:
            # define current index and get trackname
            curr_pos = playlist[counter % n]
            name = tracklist[curr_pos]
            # sleep for 5 secondes before starting playback
            time.sleep(5)
            # define timed variable such that
            # playback does not get interrupted
            delay = 5
            now = time.time()
            playing = lambda: time.time() < now + tracklength[curr_pos] + delay
            # load and play track
            track = vlc.MediaPlayer(name)
            track.play()
            # update counter
            counter += 1
            # if all tracks have been played once then create new playlist
            if counter % n == 0:
                playlist_gen()
                
        if GPIO.input(b1_pin)==0:
            stateToggle()
            time.sleep(0.5)
            
        if GPIO.input(b2_pin)==0:
            print('Shutting down')
            time.sleep(0.5)
            GPIO.output(led_pin, GPIO.LOW)
            if 'track' in locals() and track.is_playing():
                track.stop()
            break
        #time.sleep(1)

# get list of available mp3 files
os.chdir(os.path.expanduser('~/python/watchDoor/sounds'))
tracklist = [file for file in glob.glob('*.mp3')]
tracklength = [int(MP3(f).info.length) for f in tracklist]
n = len(tracklist)

# initialize playlist
playlist_gen()

# initialize replay counter
counter = 0
# initialize playing variable
playing = lambda: False

stateSetup()

watchdoor()
            
GPIO.cleanup()