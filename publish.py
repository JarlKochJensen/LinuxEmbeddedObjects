
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "jepper"
org = "pikmiginumsen"
token = "UZ5UbP4zBEdYIVCnagGPMsXvn7jEdEBZRAdBAh0NwzEVjg2ppiv-RNFZO7ToWyYRtTcp4FyPzhyEaChlE0GP7g=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
write_api = client.write_api(write_options=SYNCHRONOUS)

mqttBroker ="localhost"

client = mqtt.Client("Temperature")
client.connect(mqttBroker, port=8883)


while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("TEMPERATURE", randNumber)
    p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", randNumber)
    write_api.write(bucket=bucket, org=org, record=p)
    print("Just published " + str(randNumber) + " to topic TEMPERATURE")
    time.sleep(1)