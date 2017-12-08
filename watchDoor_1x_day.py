#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 17:14:48 2016

@author: rorix

Plays a track if motion is detected by PIR sensor.
After a single playback the script is shut down

Should be incorporated with cron job to play once per day

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
import pickle

# initialize GPIO ports
PIR_pin = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def playlist_gen(n_items):
    """
    Generate randomly shuffled playlist

    :return: <list>: list of track names
    """

    playlist = range(n_items)
    random.shuffle(playlist)
    return playlist


def playback(track):

    # sleep for 5 seconds before starting playback
    time.sleep(5)

    # load and play track
    pymixer.music.load(track)
    pymixer.music.play()

    # pygame.mixer.music.queue() is broken for me
    # using this hacky solution to address this situation
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

    After a single playback, the function exits

    :return: (empty)
    """

    # check if pickle dump file exists
    # if not, create new track and playlist
    try:
        with open('tracks.pkl', 'rb') as input:
            tracks = pickle.load(input)
            playlist = pickle.load(input)
        n = len(tracks)
    except IOError:
        tracks = [file for file in glob.glob('*.mp3')]
        n = len(tracks)
        # generate random list of indices that acts as a playlist
        playlist = playlist_gen(n)

    # set variable to abort script
    abort = False

    while True:

        if (GPIO.input(PIR_pin) == 1) and (pymixer.music.get_busy() is False):
            # define current index and get name of track
            curr_pos = playlist.pop()
            name = tracks[curr_pos]

            # start playback
            playback(name)
            
            # set abort state
            abort = True

            # write event to log file
            with open(folder + 'logfile_1x.txt', 'a') as logfile:
                logfile.write('\n' + time.strftime('%H:%M:%S'))
                logfile.write(' -- %s' % (name[:-4]))
                
            # if all tracks have been played once, create new playlist
            if len(playlist) == 0:
                # check if any files have been added in the sound directory
                if n != len(glob.glob('*.mp3')):
                    tracks = [file for file in glob.glob('*.mp3')]
                    n = len(tracks)

                # generate new playlist
                playlist = playlist_gen(n)

            # dump data in storage
            with open('tracks.pkl', 'wb') as output:
                pickle.dump(tracks, output)
                pickle.dump(playlist, output)

        elif (pymixer.music.get_busy() is False) and (abort is True):
            # if a track has been played, break
            break


# initialize pygame mixer
pymixer.init(44100, -16, 2, 4096)
pymixer.music.set_volume(0.45)  # 0.4 was a bit too quiet for noisy environment

folder = '/home/pi/watchDoor/'

# change to directory that contains sounds
os.chdir(folder + 'sounds/')

# start main function
try:
    watch_door()
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
