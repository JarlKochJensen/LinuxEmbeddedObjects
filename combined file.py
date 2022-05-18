import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

#SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
#50hz pulse dont worry about it.
servo = GPIO.PWM(12,50)
currAngl = 6
servo.start(currAngl)


def servoAngle(angle, curr):
	turns = angle*0.066666667
	if turns < currAngl:

		while curr > turns:
			curr  -= 0.3
			servo.ChangeDutyCycle(curr)
			time.sleep(0.05)
			
	elif turns > curr:
		while curr < turns:
			curr += 0.3
			servo.ChangeDutyCycle(curr)
			time.sleep(0.05)
	return curr

		


def data(mqttclient, userdata, message):
    global currAngl
    if(message.topic == "TEMPERATURE" and float(message.payload.decode("utf-8")) > 25.00):
        if currAngl < 11:
            currAngl = servoAngle(180, currAngl)
    elif(message.topic=="TEMPERATURE" and float(message.payload.decode("utf-8")) <= 25.00):
        if currAngl > 6:        
            currAngl = servoAngle(90, currAngl)
#	p = influxdb_client.Point("data").tag("location", "plantbox#1").field(message.topic, float(message.payload.decode("utf-8")))


#MQTT connection init
mqttclient = mqtt.Client("database bucket subscriber")
mqttclient.connect("localhost", port=8883)


#Starting loop for messages received
mqttclient.loop_start()
mqttclient.subscribe("TEMPERATURE")
mqttclient.subscribe("HUMIDITY")



try:
    while True:
	    mqttclient.on_message=data
except KeyboardInterrupt:
    print('interrupted!')

servo.stop()
GPIO.cleanup()
