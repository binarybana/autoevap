import time
import radiotherm
from influxdb import client as influxdb

def record_state(db, tsdata):
    data = [{'points':[[tsdata['temp'], tsdata['tstate'], tsdata['t_cool'], tsdata['hold']]],
            'name':'thermostat_data',
            'columns':['temp','state','t_cool','hold']}]
    print(data)
    db.write_points(data)

if __name__ == '__main__':
    db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')
    #ts = radiotherm.get_thermostat('thermostat-89-BD-39.local')
    ts = radiotherm.get_thermostat('192.168.1.217')

    last_state = ts.tstat['raw']
    del last_state['time']
    last_time = time.time()
    record_state(db, last_state)

    while True:
        time.sleep(5)
        state = ts.tstat['raw']
        del state['time']
        if state['tstate'] == -1:
            continue
        
        if state != last_state:
            record_state(db, state)
            last_time = time.time()
            last_state = state


