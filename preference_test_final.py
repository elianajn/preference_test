import RPi.GPIO as GPIO
from datetime import datetime
import time
import csv
import pygame as pg
import keyboard

# arr = np.empty()
arr = []
start_time = None
fam_sound = ""
unfam_sound = ""


GPIO.setmode(GPIO.BOARD)  # set up GPIO pin numeration to ordinal
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

'''
Prompts the user for full file paths to the sound files
TODO: check file type?
'''
def get_sound_files():
    global fam_sound
    global unfam_sound
    fam_sound = input("Familiar sound file path: ")
    print(str(fam_sound) + " will be used as the familiar sound")
    unfam_sound = input("Unfamiliar sound file path: ")
    print(str(unfam_sound) + " will be used as the familiar sound")
    fam_sound = "/home/pi/Desktop/birb/Lab1_bird3.wav"
    unfam_sound = "/home/pi/Desktop/birb/Lab1_bird7.wav"

'''
Plays sound, cuts off playback if method is called again before the sound finishes playing
'''
def play_sound(sound):
    pg.mixer.init()
    pg.mixer.music.load(sound)  # Load sound
    pg.mixer.music.play()
    
    
'''
Callback function for channel 11
Appends to data array if the beam is broken or unbroken
'''
def callback_beam_11(channel):
    global arr, start_time
    now = datetime.now().strftime("%H:%M:%S.%f")
    if GPIO.input(11):
        print("11 beam unbroken")
        arr.append([now, time.time() - start_time, 0, 0]) 
    else:
        print("11 beam broken")
        arr.append([now, time.time() - start_time, 1, 0])
        play_sound(fam_sound)
    
'''
Callback function for channel 15
Appends to data array if the beam is broken or unbroken
'''
def callback_beam_15(channel):
    global arr, start_time
    now = datetime.now().strftime("%H:%M:%S.%f")
    if GPIO.input(15):
        print("15 beam unbroken")
        arr.append([now, time.time() - start_time, 0, 0])
    else:
        print("15 beam broken")
        arr.append([now, time.time() - start_time, 0, 1])
        play_sound(unfam_sound)
    
'''
'''
def listen(duration):
    global start_time
    start_time = time.time()
    GPIO.add_event_detect(11, GPIO.BOTH, callback=callback_beam_11)
    GPIO.add_event_detect(15, GPIO.BOTH, callback=callback_beam_15)
    #message = input("Press enter to quit\n\n") # uncomment for manual program termination
    flag = True
    while time.time() - start_time < float(duration):
        continue
    GPIO.cleanup()
    pg.mixer.quit()


def main():
    global arr
    get_sound_files()
    animal_id = input("Please enter the animal ID, resulting CSV will be named accordingly: ")
    while animal_id == "":
        animal_id = input("Must enter animal_id: ")
    duration = int(input("How many seconds would you like the session to run? ")) #*60
    gotime = input("Ready? (y/n) ")
    if gotime == "y":
        listen(duration)
    filename = "{}.csv".format(animal_id)
    with open (filename, 'w+',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Datetime'] + ['Elapsed time'] + ['Pin 1']+ ['Pin 2'])
        for row in range(len(arr)):
            spamwriter.writerow(arr[row])
    print(arr)


if __name__ == "__main__":
    main()