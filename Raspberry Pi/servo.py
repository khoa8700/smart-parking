from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
servo = GPIO.PWM(12, 50)
servo.start(0)
sleep(2)


def openBarrier():
    servo.ChangeDutyCycle(7)
    sleep(0.5)
    servo.ChangeDutyCycle(0)


def closeBarrier():
    servo.ChangeDutyCycle(2)
    sleep(0.5)
    servo.ChangeDutyCycle(0)


def dongmocong():
    openBarrier()
    sleep(5)
    closeBarrier()
    sleep(5)
    servo.stop()
