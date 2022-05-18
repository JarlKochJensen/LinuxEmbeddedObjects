import  influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import time

def data(mqttclient, userdata, message):
	write_api = influxclient.write_api(write_options=SYNCHRONOUS)
	p = influxdb_client.Point("data").tag("location", "plantbox#1").field(message.topic, float(message.payload.decode("utf-8")))
	write_api.write(bucket=bucket, org=org, record=p)
	print("Successful upload of " + message.topic + " @ " + str(message.payload.decode("utf-8")))

#MQTT connection init
mqttclient = mqtt.Client("database bucket subscriber")
mqttclient.connect("localhost", port=8883)

#InfluxDB connection init
bucket = "GreenHouseBucket"
org = "Group15"
token = "UZ5UbP4zBEdYIVCnagGPMsXvn7jEdEBZRAdBAh0NwzEVjg2ppiv-RNFZO7ToWyYRtTcp4FyPzhyEaChlE0GP7g=="
url = "http://localhost:8086"

influxclient = influxdb_client.InfluxDBClient(
	url=url,
	token=token,
	org=org
)

#Starting loop for messages received
mqttclient.loop_start()
mqttclient.subscribe("TEMPERATURE")
mqttclient.subscribe("HUMIDITY")

while(True):
	mqttclient.on_message=data

