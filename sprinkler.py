from influxdb import client as influxdb
import time
import datetime
import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)

def run_sprinkler(db, duration):
    GPIO.output(24, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(24, GPIO.LOW)
    data = [{'points':[[duration]],
            'name':'sprinkler',
            'columns':['duration']}]
    print(data)
    db.write_points(data)

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    setup()
    while True:

        now = datetime.datetime.now()
        print("It is now {}, checking time bounds:".format(now))
        if now.hour > 10 and now.hour < 18 and now.day % 2 == 0:
            print("Running for 120 seconds!")
            run_sprinkler(db, 120)
        else:
            print("Not running, waiting for 30 minutes.")
        time.sleep(60*30)

