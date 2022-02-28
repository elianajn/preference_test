import RPi.GPIO as GPIO
import sys
from datetime import datetime, timedelta
import csv
import pygame as pg
import numpy as np

# arr = np.empty()
arr = []
fam_sound = ""
unfam_sound = ""
start_time = datetime.time()

GPIO.setmode(GPIO.BOARD)  # set up GPIO pin numeration to ordinal
GPIO.setup(11, GPIO.IN) 
GPIO.setup(15, GPIO.IN)

# print(familiar sound name?)
def get_sound_files():
    fam_sound = input("Familiar sound file name: ")
    print(str(fam_sound) + " will be used as the familiar sound")
    unfam_sound = input("Unfamiliar sound file name: ")
    print(str(unfam_sound) + " will be used as the familiar sound")


def play_sound(sound):
        pg.mixer.init()
        pg.mixer.music.load(sound)  # Load go sound
        pg.mixer.music.play()
        while pg.mixer.music.get_busy():  # Keep on hold while playing
            continue
        pg.mixer.quit()


'''
https://raspi.tv/2014/rpi-gpio-update-and-detecting-both-rising-and-falling-edges
'''
def listen():
    duration = int(input("How long would you like the session to run? (min)")) * 1000 * 60
    while (datetime.time() - start_time) < duration:
        if GPIO.add_event_detect(11, GPIO.BOTH):
            if GPIO.input(11):     # if port 11 == 1
                play_sound(fam_sound)
                arr.append([datetime.datetime(), datetime.time() - start_time, True, False])  
                print "Rising edge detected on 11"  
            else:                  # if port 11 != 1  
                arr.append([datetime.datetime(), datetime.time() - start_time, False, False])
                print "Falling edge detected on 11" 
        if GPIO.add_event_detect(15, GPIO.BOTH):
            if GPIO.input(15):     # if port 15 == 1
                play_sound(unfam_sound)
                arr.append([datetime.datetime(), datetime.time() - start_time, False, True])
                print "Rising edge detected on 15"  
            else:                  # if port 15 != 1
                arr.append([datetime.datetime(), datetime.time() - start_time, False, False])
                print "Rising edge detected on 15"  


def main():
    get_sound_files()
    animal_id = input("Please enter the animal ID, resulting CSV will be named accordingly: ")
    while animal_id is "":
        animal_id = input("Must enter animal_id: ")
    filename = "{}.csv".format(animal_id)
    with open (filename, 'w+',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Datetime'] + ['Elapsed time'] + ['Pin 1']+ ['Pin 2'])
        for row in range(len(arr)):
           spamwriter.writerow(arr[row])


if __name__ == "__main__":
    main()