#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 17:14:48 2016

@author: rorix

RPi Pinout:
    PIR Data: Pin 15
    5V Power: Pin 2
    Ground: Pin 6
"""

import RPi.GPIO as GPIO
import glob
import os
import random
import time
import pygame.mixer as pymixer

# initialize GPIO ports
PIR_pin = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def playlist_gen(n_items):
    """
    Generate randomly shuffled playlist

    :return: <list>: list of track names
    """

    playlist_tmp = range(n_items)
    random.shuffle(playlist_tmp)
    return playlist_tmp


def playback(track):

    # sleep for 5 seconds before starting playback
    time.sleep(5)

    # load and play track
    pymixer.music.load(track)
    pymixer.music.play()
    # add mp3 that contains 45 seconds of silence
    # so two tracks don't play back to back

    # ---- queue is broken ----
    # pymixer.music.queue('00_silence.mp3')

    while pymixer.music.get_busy():
        time.sleep(0.75)

    pymixer.music.load('00_silence.mp3')
    pymixer.music.play()


def watch_door():
    """
    This is the main function. It consists of an endless loop
    that checks, whether motion has been detected by the PIR sensor.
    If it detects motion (PIR_pin is high) and no playback is
    currently active, it plays a track from the playlist

    After each track, there is a delay of 45 seconds, before the
    next track is played.

    :return: (empty)
    """

    # initialize counter variable
    counter = 0

    # get available tracks
    tracks = [file for file in glob.glob('*.mp3')]
    n = len(tracks)
    # generate random list of indices that acts as a playlist
    playlist = playlist_gen(n)

    while True:

        if GPIO.input(PIR_pin) == 1 and pymixer.music.get_busy() == 0:
            # define current index and get name of track
            curr_pos = playlist[counter % n]
            name = tracks[curr_pos]

            # start playback
            playback(name)
            
            # update counter
            counter += 1

            # write event to log file
            with open(folder + 'logfile.txt', 'a') as logfile:
                logfile.write('\n' + time.strftime('%H:%M:%S'))
                logfile.write(' -%d - %s' % (counter, name[:-4]))
                
            # if all tracks have been played once, create new playlist
            if counter % n == 0:
                # check if any files have been added in the sound directory
                if n != len(glob.glob('*.mp3')):
                    tracks = [file for file in glob.glob('*.mp3')]
                    n = len(tracks)

                # generate new playlist
                playlist = playlist_gen(n)


# initialize pygame mixer
pymixer.init(44100, -16, 2, 4096)
pymixer.music.set_volume(0.5)  # 0.4 was a bit too quiet for noisy environment

folder = '/home/pi/watchDoor/'

# change to directory that contains sounds
os.chdir(folder + 'sounds/')

# initialize log file
with open(folder + 'logfile.txt', 'a') as logfile:
    logfile.write('\n\n=======================')
    logfile.write('\nStarting Script')
    logfile.write('\nCurrent date:')
    logfile.write(time.strftime('%a, %d %b %Y %H:%M:%S'))

# start main function
try:
    watch_door()
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
