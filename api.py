from influxdb import client as influxdb
import glob
import time
import urllib2
import json

key = open('wgkey.txt').read().strip()
url = "http://api.wunderground.com/api/{}/conditions/q/77845.json".format(key)

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    while True:
        resp = urllib2.urlopen(url).read()
        #respdata = json.loads(resp.read())
        data = [{'points':[[resp]],
                'name':'wunderground',
                'columns':['data']}]
        db.write_points(data)
        print("Wunderground data written, waiting 30 minutes...")
        time.sleep(60*30)


