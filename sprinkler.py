from influxdb import client as influxdb
import time
import RPi.GPIO as GPIO

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)

def run_sprinkler(db, duration):
    data = [{'points':[[duration]],
            'name':'sprinkler',
            'columns':['duration']}]
    print(data)
    db.write_points(data)
    GPIO.output(24, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(24, GPIO.LOW)

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    setup()
    run_sprinkler(db, 60)

