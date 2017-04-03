#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 17:16:48 2016

@author: rorix
this is a test for a motion detection script.
to activate it, run the script. then answer the prompt with y to activate
afterwards, sound clipds should launch, when you write motion
to exit, type exit
"""

import time
import random
#import pygame.mixer
import vlc
import glob, os
from mutagen.mp3 import MP3

def activeSetup():
    global active
    active=0
    print("System initialized.\nCurrently not active.")

def activeState():
    global active
    if active==1:
        active=0
        print("Currently not active.")
        
    elif active==0:
        print("Activating in 3 seconds.")
        
        for x in range(0,3):
            print('%d')%(3-x)
            time.sleep(1)
        active=1
    else:
        return
        
def playlist_gen():
    global playlist
    playlist = range(n)
    random.shuffle(playlist)
                

#pygame.mixer.init(44100,-16,2,1024)
#pygame.mixer.music.set_volume(1.0)

os.chdir('/home/rorix/Downloads/FF-intro')
tracklist = [f for f in glob.glob("*.mp3")]
tracklength = [int(MP3(f).info.length)+3 for f in tracklist]
n = len(tracklist)

activeSetup()
playlist_gen()

playing = lambda: False
counter = 0

while True:
    myvar = raw_input('Enter your input (wut):')
    if active==1 and myvar=='motion' and playing()==False:
        idx = playlist[counter % n]
        name = tracklist[idx]
        now = time.time()
        playing = lambda: time.time() < now + tracklength[idx]        
        #pygame.mixer.music.load(name)
        #pygame.mixer.music.play()
        track = vlc.MediaPlayer(name)
        track.play()
        track.audio_set_volume(125)
        counter += 1
        if counter % n == 0:
            playlist_gen()
    elif myvar=='toggle':
        activeState()
        time.sleep(0.5)
    elif myvar=='stop':
        #pygame.mixer.music.stop()
        if track.isplaying():
            track.stop()
        playing = lambda: False
    elif myvar=='exit':
        print('Stopping inner loop')
        #pygame.mixer.music.stop()
        if track.isplaying():
            track.stop()
        break
        