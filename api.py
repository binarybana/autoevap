from influxdb import client as influxdb
import glob
import time
import urllib2
import json

key = open('wgkey.txt').read().strip()
#url = "http://api.wunderground.com/api/{}/conditions/q/77845.json".format(key)
url = "http://api.wunderground.com/api/{}/conditions/q/pws:KTXCOLLE20.json".format(key)

def grab_and_record(url):
    try:
        resp = urllib2.urlopen(url).read()
    except:
        return
    data = [{'points':[[resp]],
            'name':'wunderground',
            'columns':['data']}]
    db.write_points(data)

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    while True:
        grab_and_record(url)
        print("Wunderground data written, waiting 30 minutes...")
        time.sleep(60*10)


