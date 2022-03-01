import RPi.GPIO as GPIO
from datetime import datetime
import time
import csv
import pygame as pg

# arr = np.empty()
arr = []
fam_sound = ""
unfam_sound = ""


GPIO.setmode(GPIO.BOARD)  # set up GPIO pin numeration to ordinal
GPIO.setup(11, GPIO.IN) 
GPIO.setup(15, GPIO.IN)

# print(familiar sound name?)
def get_sound_files():
    global fam_sound
    global unfam_sound
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
def listen(duration):
    global arr
    start_time = time.time()
    print(fam_sound)
    #GPIO.add_event_detect(15, GPIO.BOTH)
    #while ((start_time.strftime("%H") - time_now.strftime("%H"))*60*60 +(start_time.strftime("%M") - time_now.strftime("%M"))*60 + (start_time.strftime("%S") - time_now.strftime("%S")) )*1000+ (start_time.strftime("%f") - time_now.strftime("%f")) < duration:
    print(fam_sound)
    GPIO.add_event_detect(11, GPIO.FALLING)
    while time.time() - start_time < float(duration):
        if GPIO.event_detected(11):
            print((time.time() - start_time))
            now = datetime.now().strftime("%H:%M:%S.%f")
            if not GPIO.input(11):     # if port 11 == 1
                play_sound(fam_sound)
                arr.append([now, time.time() - start_time, True, False])  #TODO: make sure that this is what you want stored in respect to rising/falling
                print("Falling edge detected on 11")
                GPIO.remove_event_detect(11)
                GPIO.add_event_detect(11, GPIO.RISING)
            else:                  # if port 11 != 1  
                arr.append([now, time.time() - start_time, False, False])
                print("Rising edge detected on 11")
                GPIO.remove_event_detect(11)
                GPIO.add_event_detect(11, GPIO.FALLING)
#        if GPIO.event_detected(15):
 #           print("hit 15")
  #          now = datetime.now().strftime("%H:%M:%S.%f")
   #         if GPIO.input(15):     # if port 15 == 1
    #            play_sound(unfam_sound)
     #           arr.append([now, time.time() - start_time, False, True])
      #          print("Rising edge detected on 15")
       #     else:                  # if port 15 != 1
        #        arr.append([now, time.time() - start_time, False, False])
         #       print("Rising edge detected on 15")
    GPIO.remove_event_detect(11)
    #GPIO.remove_event_detect(15)
    GPIO.cleanup(11)
    #GPIO.cleanup(15)


def main():
    global arr
    get_sound_files()
    animal_id = input("Please enter the animal ID, resulting CSV will be named accordingly: ")
    while animal_id == "":
        animal_id = input("Must enter animal_id: ")
    duration = int(input("How many seconds would you like the session to run? ")) #*60
    gotime = input("Ready?(y/n) ")
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