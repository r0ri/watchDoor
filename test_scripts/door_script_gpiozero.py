#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 15:27:46 2016

@author: rorix
"""

from gpiozero import LED, Button, MotionSensor
import time, os, glob, random
import pygame.mixer
from mutagen.mp3 import MP3

pir = MotionSensor(15, queue_len=1)
led = LED(7)
toggle_button = Button(11)
off_button = Button(13)
led.off()

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
            led.on
            time.sleep(0.5)
            led.off
            time.sleep(0.5)
        active = 1
        led.on
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
        if pir.motion_detected and playing()==False and active==1:
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
            pygame.mixer.music.load(name)
            pygame.mixer.music.play()
            # update counter
            counter +=1
            # if all tracks have been played once then create new playlist
            if counter % n == 0:
                playlist_gen()
                
        if toggle_button.is_pressed:
            stateToggle()
            time.sleep(0.5)
            
        if off_button.is_pressed:
            print('Shutting down')
            time.sleep(0.5)
            led.off
            pygame.mixer.music.stop()
            break
        #time.sleep(1)
    
    
# initialize pygame mixer
pygame.mixer.init(44100,-16,2,4096)
pygame.mixer.music.set_volume(1.0)
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