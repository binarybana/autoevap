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

rundur = 60
restdur = 60*10

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    setup()
    while True:

        now = datetime.datetime.now()
        print("It is now {}, checking time bounds:".format(now))
        if now.hour > 10 and now.hour < 19 and now.day % 2 == 0:
            print("Running for {} seconds!".format(rundur))
            run_sprinkler(db, rundur)
            time.sleep(restdur-rundur)
        else:
            print("Not running, waiting for {} minutes.".format(restdur/60))
            time.sleep(restdur)

