from influxdb import client as influxdb
import glob
import time

lut = {'28-0000037750a3':'in', '28-000003777657':'out', '28-00000377770e':'attic'}

def read_temp(therm):
    res = open('{}/w1_slave'.format(therm)).readlines()
    if res[0].find('YES') == -1:
        return None
    return float(res[1].split('=')[1])/1000.0

def read_all_temps():
    therms = []
    temps = []
    for therm in glob.glob('/sys/bus/w1/devices/28*'):
        temp = read_temp(therm)
        if temp != None:
            temps.append(temp)
            therms.append(lut[therm.split('/')[-1]])
    return therms, temps

if __name__=='__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    while True:
        therms, temps = read_all_temps()
        data = [{'points':[temps],
                'name':'dstemps',
                'columns':therms}]
        print(data)
        db.write_points(data)
        time.sleep(60)

