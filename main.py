import RPi.GPIO as GPIO
import time
import speech_recognition as sr


# Define servo angle function
def set_servo_angle(angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)


# create a speech recognizer object
r = sr.Recognizer()

# define the audio source
with sr.Microphone() as source:
    print("Say something!")
    r.pause_threshold = 1
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
# recognize speech using Google Speech Recognition
try:
    command = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said " + command)
    # check if command matches the phrase "turn the lights on"
    if "turn the lights off" in command:
        # set up GPIO for servo motor
        servo_pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        # define servo motor properties
        pwm = GPIO.PWM(servo_pin, 50)
        pwm.start(0)
        # Turn servo 90 degrees clockwise
        set_servo_angle(90)
        # Wait for 0.5 second
        time.sleep(0.5)
        # Return servo to original position
        set_servo_angle(0)
        time.sleep(0.5)
        # clean up GPIO when finished
        pwm.stop()
        GPIO.cleanup()
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
