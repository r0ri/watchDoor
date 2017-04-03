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

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def playlist_gen():
    playlist = range(n)
    random.shuffle(playlist)
    return playlist

def playback(track, tracklen):
    global playing
    # sleep for 5 seconds before starting playback
    time.sleep(5)
    # define timed variable so that playback does not get
    # interrupted. also set delay after playback
    delay = 45
    now = time.time()
    playing = lambda: time.time() < now + tracklen + delay
    # load and play track
    pygame.mixer.music.load(track)
    pygame.mixer.music.play()
    
def watchdoor():
    global counter
    global playing
    while True:
        if GPIO.input(PIR_pin)==1 and playing()==False:
            #define current index and get trackname
            curr_pos = playlist[counter % n]
            name = tracklist[curr_pos]
            
            playback(name, tracklength[curr_pos])
            
            # update counter
            counter += 1
            
            with open('/home/pi/python/watchDoor/logfile', 'a') as logfile:
                logfile.write('\n' + time.strftime('%H:%M:%S'))
                logfile.write(' -%d - %s' % (counter, name[:-4]))
                
            # if all tracks have been played once then create new playlist
            if counter % n == 0:
                playlist_gen()

# initialize pygame mixer
pygame.mixer.init(44100,-16,2,4096)
pygame.mixer.music.set_volume(0.4)

# get list of available mp3 files and their length
os.chdir('/home/pi/python/watchDoor/sounds')
tracklist = [file for file in glob.glob('*.mp3')]
tracklength = [int(MP3(f).info.length) for f in tracklist]
n = len(tracklist)

with open('/home/pi/python/watchDoor/logfile.txt', 'a') as logfile:
    logfile.write('\n\n=======================')
    logfile.write('\nStarting Script')
    logfile.write('\nCurrent date:')
    logfile.write(time.strftime('%a, %d %b %Y %H:%M:%S'))

# initialize playlist
playlist = playlist_gen()
# initialize replay counter
counter = 0
# initialize playing variable
playing = lambda:False

try:
    watchDoor()
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()