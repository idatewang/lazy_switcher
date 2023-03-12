# add python script.py to setup sequence


import RPi.GPIO as GPIO
import time
import speech_recognition as sr

# set up GPIO for servo motor
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# define servo motor properties
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(2.5)

# create a speech recognizer object
r = sr.Recognizer()

# define the audio source (e.g. microphone)
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    command = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + command)

    # check if command matches the phrase "turn the lights on"
    if "turn the lights on" in command:
        # move servo motor 90 degrees
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        pwm.ChangeDutyCycle(2.5)
        time.sleep(1)
        
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

# clean up GPIO when finished
pwm.stop()
GPIO.cleanup()
