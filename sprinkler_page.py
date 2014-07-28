import time
import cherrypy

import RPi.GPIO as GPIO

from influxdb import client as influxdb

class SprinklerControl(object):
    def __init__(self, db):
        self.db = db
        self.starttime = None
        self.status = False

    @cherrypy.expose
    def index(self, action=None):
        if action == 'on':
            if self.status:
                print('Sprinkler ALREADY on!')
            else:
                self.sprinkler_on()
        elif action == 'off':
            if self.status:
                self.sprinkler_off()
            else:
                print('Sprinkler ALREADY off!')

        return """<html>
          <head><title>Knight Sprinkler Control Panel</title>
          <style type="text/css">
          button {
          height: 4em;
          width: 12em;
          font-size: 2em;
          }
          h1 {
          font-size: 3em;
          }
          </style></head>
          <body>
          <h1>Knight Sprinkler Control Panel</h1>
            <form method="get" action="index">
            <input type="hidden" name="action" value="on" />
              <button type="submit" class="button">SPRINKLER ON</button>
            </form>
            <form method="get" action="index">
            <input type="hidden" name="action" value="off" />
              <button type="submit" class="button">SPRINKLER OFF</button>
            </form>
            <p>Sprinkler is currently: """+ ('ON' if self.status else 'OFF') + """</p>
          </body>
        </html>"""

    def record_sprinkler(self, duration):
        data = [{'points':[[duration]],
                'name':'sprinkler',
                'columns':['duration']}]
        print(data)
        db.write_points(data)

    def sprinkler_on(self):
        GPIO.output(24, GPIO.HIGH)
        self.status = True
        self.starttime = time.time()
        print("Sprinkler ON")

    def sprinkler_off(self):
        GPIO.output(24, GPIO.LOW)
        self.status = False
        duration = time.time() - self.starttime
        self.starttime = None
        print("Duration: {} seconds".format(duration))
        print("Sprinkler OFF")
        self.record_sprinkler(duration)

def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    gpio_setup()
    cherrypy.config.update({'server.socket_port': 80, 'server.socket_host':'0.0.0.0'})
    cherrypy.quickstart(SprinklerControl(db))

