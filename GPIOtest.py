import RPi.GPIO as GPIO
import time

#SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
#50hz pulse dont worry about it.
servo = GPIO.PWM(12,50)
currAngl = 6
servo.start(currAngl)


def servoAngle(angle, curr):
	turns = angle*0.066666667
	currAngl = curr
	if turns < currAngl:

		while currAngl > turns:
			currAngl  -= 0.3
			servo.ChangeDutyCycle(currAngl)
			time.sleep(0.05)
			
	elif turns > currAngl:
		while currAngl < turns:
			currAngl += 0.3
			servo.ChangeDutyCycle(currAngl)
			time.sleep(0.05)
	return currAngl

		

currAngl = servoAngle(180, currAngl)
time.sleep(2)
currAngl = servoAngle(90, currAngl)
time.sleep(2)

servo.stop()
GPIO.cleanup()
