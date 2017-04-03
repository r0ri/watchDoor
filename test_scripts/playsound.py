#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 13:31:06 2016

@author: rorix
"""

# import Rpi.GPIO as GPIO
import time
import random
import pygame.mixer

def activeSetup():
    global active
    active=0
    print("Currently not active.")

def activeState():
    global active
    if active==1:
        active=0
        # GPIO.output(7,GPIO.LOW)
        print("Currently not active.")
        
    elif active==0:
        print("Activating in 3 seconds.")
        
        for x in range(0,3):
            # GPIO.outpu(7,GPIO.HIGH)
            print('%d')%(3-x)
            time.sleep(1)
            
            # GPIO.output(7,GPIO.LOW)
            time.sleep(0.5)
        active=1
        #GPIO.output(7, GPIO.HIGH)
    else:
        return
        
def watchDoor():
    global playing
    global active
    playing = False
    while True:
        if active==1 and playing == False: #and GPIO.input(15)==1
            playing = True
            idx = random.randint(0,len(tracklist)-1)
            name = tracklist[idx]
            pygame.mixer.music.load("/home/rorix/Downloads/"+name)
            pygame.mixer.music.play()
            time.sleep(tracklength[idx])
        else:
            myvar = raw_input('Enter your input (inner):')
            if myvar=='toggle':
                activeState()
                time.sleep(0.5)
            elif myvar=='r':
                playing=False
            elif myvar=='exit':
                print('Stopping inner loop')
                active = 0
                pygame.mixer.music.stop()
                break
            

#
activeSetup()
pygame.mixer.init(44100,-16,2,1024)
pygame.mixer.music.set_volume(1.0)
tracklist = ['Sp1.mp3', 'Sp2.mp3']
tracklength = [80, 11] # track length in seconds

while True:
    if active==1:
        watchDoor()
        #break
    else:
        myvar = raw_input('Enter your input (outer): ')
        if myvar == 'toggle':
            activeState()
        elif myvar == 'exit':
            print('Stopping outer loop')
            time.sleep(1)
            pygame.mixer.music.stop()
            break