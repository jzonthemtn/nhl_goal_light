import random
import platform
import pygame

if "armv" in platform.machine() :
    # import GPIO if running on RPI
    import RPi.GPIO as GPIO
else :
    # import gpio_mock if not running on RPI
    from lib import gpio_mock as GPIO


def setup():
    """ Function to setup raspberry pi GPIO mode and warnings. PIN 7 OUT and PIN 11 IN """

    # Setup GPIO on raspberry pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    GPIO.setup(21, GPIO.OUT, initial=GPIO.HIGH) # Tell the program you want to use pin number 7 as output. Relay is ACTIVE LOW, so OFF is HIGH
    #GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO 11 as a PULL DOWN switch
    #GPIO.add_event_detect(11, GPIO.RISING, activate_goal_light, 5000)


def activate_goal_light(gpio_event_var=0):
    """ Function to activate GPIO for goal light and plar random audio clip. """
    print "Activating light"
    songrandom = random.randint(3, 3) #Set random numbers depending on number of audio clips available
    # Prepare commande to play sound (change file name if needed)
    pygame.mixer.init()
    pygame.mixer.music.load('/home/pi/nhl_goal_light/audio/goal_horn_{SongId}.mp3'.format(SongId=str(songrandom)))
    pygame.mixer.music.play()
    print "Turning on light"
    GPIO.output(21, GPIO.LOW) #Turn on light, active low relay, so on is low
    while pygame.mixer.music.get_busy() == True:
        continue
    GPIO.output(21, GPIO.HIGH) #Turn off light


def cleanup():
    """ Function to cleanup raspberry pi GPIO at end of code """

    # Restore GPIO to default state
    GPIO.remove_event_detect(15) #Add to end of function
    GPIO.cleanup()
    print("GPIO cleaned!")
