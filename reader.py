import json

import pandas as pa
import pylab as p
import matplotlib.dates as dates

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
#temps.columns = 'Inside Outside Attic'.split()
tstat = dfquery(db,'select * from thermostat_data')
sprink = dfquery(db,'select * from sprinkler')
wunder = dfquery(db,'select data from wunderground')

fig, ax = p.subplots(nrows=1, sharex=True)
ax = [ax]

tstat['temp'].plot(ax=ax[0], linewidth=2, label='tstat')

ftemps = temps*9/5.0+32

for col in ftemps.columns:
    ax[0].plot_date(ftemps.index.to_pydatetime(), ftemps[col], '-', linewidth=2,
        label=col)
#ax.xaxis.set_minor_locator(dates.WeekdayLocator(byweekday=(1),
                                                #interval=1))
ax[0].xaxis.set_major_formatter(dates.DateFormatter('%b-%d\n%X'))
#ax.xaxis.set_minor_formatter(dates.DateFormatter('%d\n%a'))
ax[0].xaxis.grid(True)
ax[0].yaxis.grid()
#ax.xaxis.set_major_locator(dates.MonthLocator())
#ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n\n%b\n%Y'))

#ftemps.plot(ax=ax,linewidth=3)

running = False
for t in tstat.index:
    if not running and tstat.loc[t,'state'] == 2:
        start = t
        running = True
    elif running and tstat.loc[t,'state'] == 0:
        stop = t
        ax[0].axvspan(start, stop, alpha=0.3)
        running = False

const = 72
for t in sprink.index:
    ax[0].plot([t-pa.DateOffset(seconds=sprink.loc[t,'duration']),t],
            [const,const],
            linewidth=3,
            color='k')

wunderparse = wunder.data.map(lambda x: json.loads(x)['current_observation'])
wex = wunderparse.iloc[0]
wall = pa.DataFrame.from_dict(wunderparse.to_dict()).T

wall.temp_f.plot(ax=ax[0], label='Wunderground', linewidth=2)

p.legend(loc='best')
p.tight_layout()
p.show()
