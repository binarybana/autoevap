import json
import pandas as pa

from influxdb import client as influxdb
from ggplot import *

db = influxdb.InfluxDBClient(host='raspberrypi', database='hvac')

def rm_col(df, col):
    if col in df:
        df.drop(col,axis=1,inplace=True)

def dfquery(db, query):
    res = db.query(query)
    df = pa.DataFrame(res[0]['points'], columns=res[0]['columns'])
    df.index = pa.to_datetime(df.iloc[:,0], unit='s', utc=False)
    df.index = df.index.tz_localize('UTC')
    df.index = df.index.tz_convert("US/Central")
    rm_col(df, 'time')
    rm_col(df, 'sequence_number')
    return df

def ptemps(db, when, ax):
    temps = dfquery(db,'select * from dstemps {}'.format(when))
    ##temps = dfquery(db,'select mean("in"),mean("out"),mean("attic") from dstemps group by time(30m)')
    #temps.columns = 'Inside Outside Attic'.split()
    ftemps = temps*9/5.0+32
    for col in ftemps.columns:
        ax[0].plot_date(ftemps.index.to_pydatetime(), ftemps[col], '-', linewidth=2,
            label=col)
    #ftemps.plot(ax=ax,linewidth=3)

def ptstat(db, when, ax):
    tstat = dfquery(db,'select * from thermostat_data {}'.format(when))
    tstat['temp'].plot(ax=ax[0], linewidth=2, label='tstat')
    running = False
    for t in tstat.index:
        if not running and tstat.loc[t,'state'] == 2:
            start = t
            running = True
        elif running and tstat.loc[t,'state'] == 0:
            stop = t
            ax[0].axvspan(start, stop, alpha=0.3)
            running = False

def psprink(db, when, ax):
    sprink = dfquery(db,'select * from sprinkler {}'.format(when))
    const = 72
    for t in sprink.index:
        ax[0].plot([t-pa.DateOffset(seconds=sprink.loc[t,'duration']),t],
                [const,const],
                linewidth=3,
                color='k')

def pwunder(db, when):
    wunder = dfquery(db,'select data from wunderground {}'.format(when))
    wunderparse = wunder.data.map(lambda x: json.loads(x)['current_observation'])
    wex = wunderparse.iloc[0]
    wall = pa.DataFrame.from_dict(wunderparse.to_dict()).T
    wall.index.name = 'date'
    wall = wall.reset_index()

    g = ggplot(wall, aes('date','temp_f')) + geom_line()
    print g
    print ggplot(wall, aes('date','solarradiation')) + geom_line()
    return g,wall

when = ' where time > now() - 16h'

#ptemps(db, when, ax)
#ptstat(db, when, ax)
#psprink(db, when, ax)
g,wall = pwunder(db, when)

