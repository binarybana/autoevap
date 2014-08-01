import json

import pandas as pa
import pylab as p

from influxdb import client as influxdb

db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')

def rm_col(df, col):
    if col in df:
        df.drop(col,axis=1,inplace=True)

def dfquery(db, query):
    res = db.query(query)
    df = pa.DataFrame(res[0]['points'], columns=res[0]['columns'])
    df.index = pa.to_datetime(df.iloc[:,0], unit='s')
    rm_col(df, 'time')
    rm_col(df, 'sequence_number')
    return df

temps = dfquery(db,'select * from dstemps')
##temps = dfquery(db,'select mean("in"),mean("out"),mean("attic") from dstemps group by time(30m)')
temps.columns = 'Inside Outside Attic'.split()
tstat = dfquery(db,'select * from thermostat_data')
sprink = dfquery(db,'select * from sprinkler')

ax=tstat['temp'].plot(linewidth=2, label='tstat')

ftemps = temps*9/5.0+32

ftemps.plot(ax=ax,linewidth=3)

running = False
for t in tstat.index:
    if not running and tstat.loc[t,'state'] == 2:
        start = t
        running = True
    elif running and tstat.loc[t,'state'] == 0:
        stop = t
        p.axvspan(start, stop, alpha=0.3)
        running = False

const = 72
for t in sprink.index:
    p.plot([t-pa.DateOffset(seconds=sprink.loc[t,'duration']),t],
            [const,const],
            linewidth=3,
            color='k')

p.show()
