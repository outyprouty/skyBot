import xmltodict, requests
from datetime import datetime
import dotenv, os
from datetime import datetime, timedelta
import json
import pytz
import sys

url = "https://forecast.weather.gov/MapClick.php?lat=39.2906&lon=-76.6093&FcstType=digitalDWML"

os.system("curl \"{}\" > noaa.xml".format(url))

xmlData = open("noaa.xml", 'r').read()
data = xmltodict.parse(xmlData)

hrs=data['dwml']['data']['time-layout']['start-valid-time']

ccs=data['dwml']['data']['parameters']['cloud-amount']['value']

nccTups = []

for time,cc in zip(hrs, ccs):
    dtime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
    try:
        nccTups.append((dtime.strftime("%Y%m%dT%H%M %a"),"nCC:{:03d}".format(int(cc)) ))
    except TypeError:
        continue


#######


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    if t == None:
        return None
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

# ripped from https://docs.tomorrow.io/reference/data-layers-core
moonPhase = \
{0: "New",
1: "Waxing Crescent",
2: "First Quarter",
3: "Waxing Gibbous",
4: "Full",
5: "Waning Gibbous",
6: "Third Quarter",
7: "Waning Crescent"}

url = "https://api.tomorrow.io/v4/timelines"

dotenv.load_dotenv()

# #Get sunset data
querystring = {
"location":"6477cc2713627de22c3eb131",
"fields":["sunsetTime", "sunriseTime", "moonPhase", "moonriseTime", "moonsetTime"],
"timesteps":"1d",
#"startTime":datetime.now().strftime("%Y-%m-%d"),
#"endTime":(datetime.now()+timedelta(days=3)).strftime("%Y-%m-%d"),
"timezone":"America/New_York",
"apikey":os.getenv("tomorrowAPIKey")}

response = requests.request("GET", url, params=querystring)
sunset=response.text
#sunset='{"data":{"timelines":[{"timestep":"1d","endTime":"2023-06-05T06:00:00-04:00","startTime":"2023-05-31T06:00:00-04:00","intervals":[{"startTime":"2023-05-31T06:00:00-04:00","values":{"moonPhase":3,"moonriseTime":"2023-05-31T20:53:11Z","moonsetTime":"2023-05-31T07:28:51Z","sunriseTime":"2023-05-31T09:54:00Z","sunsetTime":"2023-06-01T00:14:00Z"}},{"startTime":"2023-06-01T06:00:00-04:00","values":{"moonPhase":3,"moonriseTime":"2023-06-01T22:00:16Z","moonsetTime":"2023-06-01T07:53:45Z","sunriseTime":"2023-06-01T09:54:00Z","sunsetTime":"2023-06-02T00:15:00Z"}},{"startTime":"2023-06-02T06:00:00-04:00","values":{"moonPhase":3,"moonriseTime":"2023-06-02T23:11:19Z","moonsetTime":"2023-06-02T08:21:33Z","sunriseTime":"2023-06-02T09:54:00Z","sunsetTime":"2023-06-03T00:15:00Z"}},{"startTime":"2023-06-03T06:00:00-04:00","values":{"moonPhase":4,"moonriseTime":null,"moonsetTime":"2023-06-03T08:57:27Z","sunriseTime":"2023-06-03T09:54:00Z","sunsetTime":"2023-06-04T00:15:00Z"}},{"startTime":"2023-06-04T06:00:00-04:00","values":{"moonPhase":4,"moonriseTime":"2023-06-04T00:24:16Z","moonsetTime":"2023-06-04T09:40:47Z","sunriseTime":"2023-06-04T09:54:00Z","sunsetTime":"2023-06-05T00:16:00Z"}},{"startTime":"2023-06-05T06:00:00-04:00","values":{"moonPhase":4,"moonriseTime":"2023-06-05T01:34:53Z","moonsetTime":"2023-06-05T10:35:45Z","sunriseTime":"2023-06-05T09:54:00Z","sunsetTime":"2023-06-06T00:16:00Z"}}]}]}}'
sunset.replace('null', "None")
sunset=json.loads(sunset)

# #Get cloud cover data
querystring = {
"location":"6477cc2713627de22c3eb131",
"fields":["cloudCover"],
"units":"metric",
#"startTime":datetime.now().strftime("%Y-%m-%d"),
#"endTime":(datetime.now()+timedelta(days=3)).strftime("%Y-%m-%d"),
"timesteps":"1h",
"timezone":"America/New_York",
"apikey":os.getenv("tomorrowAPIKey")}

response = requests.request("GET", url, params=querystring)
print(response.text)
cc=json.loads(response.text)
#cc={"data":{"timelines":[{"timestep":"1h","endTime":"2023-06-02T20:00:00-04:00","startTime":"2023-05-30T20:00:00-04:00","intervals":[{"startTime":"2023-05-30T20:00:00-04:00","values":{"cloudCover":19}},{"startTime":"2023-05-30T21:00:00-04:00","values":{"cloudCover":2}},{"startTime":"2023-05-30T22:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-30T23:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T00:00:00-04:00","values":{"cloudCover":1}},{"startTime":"2023-05-31T01:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T02:00:00-04:00","values":{"cloudCover":17}},{"startTime":"2023-05-31T03:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T04:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T05:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T06:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T07:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T08:00:00-04:00","values":{"cloudCover":3}},{"startTime":"2023-05-31T09:00:00-04:00","values":{"cloudCover":8}},{"startTime":"2023-05-31T10:00:00-04:00","values":{"cloudCover":3}},{"startTime":"2023-05-31T11:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T12:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T13:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T14:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T15:00:00-04:00","values":{"cloudCover":1}},{"startTime":"2023-05-31T16:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T17:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T18:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T19:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T20:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T21:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T22:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-05-31T23:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T00:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T01:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T02:00:00-04:00","values":{"cloudCover":1.2}},{"startTime":"2023-06-01T03:00:00-04:00","values":{"cloudCover":8.36}},{"startTime":"2023-06-01T04:00:00-04:00","values":{"cloudCover":76.65}},{"startTime":"2023-06-01T05:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-01T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-01T07:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-01T08:00:00-04:00","values":{"cloudCover":97.77}},{"startTime":"2023-06-01T09:00:00-04:00","values":{"cloudCover":81.83}},{"startTime":"2023-06-01T10:00:00-04:00","values":{"cloudCover":46.81}},{"startTime":"2023-06-01T11:00:00-04:00","values":{"cloudCover":7.18}},{"startTime":"2023-06-01T12:00:00-04:00","values":{"cloudCover":2.56}},{"startTime":"2023-06-01T13:00:00-04:00","values":{"cloudCover":1.6}},{"startTime":"2023-06-01T14:00:00-04:00","values":{"cloudCover":1.44}},{"startTime":"2023-06-01T15:00:00-04:00","values":{"cloudCover":1.48}},{"startTime":"2023-06-01T16:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T17:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T18:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T19:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T20:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T21:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T22:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-01T23:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-02T00:00:00-04:00","values":{"cloudCover":0.08}},{"startTime":"2023-06-02T01:00:00-04:00","values":{"cloudCover":1.28}},{"startTime":"2023-06-02T02:00:00-04:00","values":{"cloudCover":8.13}},{"startTime":"2023-06-02T03:00:00-04:00","values":{"cloudCover":28.43}},{"startTime":"2023-06-02T04:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-02T05:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-02T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-02T07:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-02T08:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-02T09:00:00-04:00","values":{"cloudCover":87.56}},{"startTime":"2023-06-02T10:00:00-04:00","values":{"cloudCover":48.46}},{"startTime":"2023-06-02T11:00:00-04:00","values":{"cloudCover":5.72}},{"startTime":"2023-06-02T12:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-02T13:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-02T14:00:00-04:00","values":{"cloudCover":0}},{"startTime":"2023-06-02T15:00:00-04:00","values":{"cloudCover":35.94}},{"startTime":"2023-06-02T16:00:00-04:00","values":{"cloudCover":33.59}},{"startTime":"2023-06-02T17:00:00-04:00","values":{"cloudCover":34.38}},{"startTime":"2023-06-02T18:00:00-04:00","values":{"cloudCover":14.84}},{"startTime":"2023-06-02T19:00:00-04:00","values":{"cloudCover":32.03}},{"startTime":"2023-06-02T20:00:00-04:00","values":{"cloudCover":22.66}}]}]}}

tmp = datetime.strptime(sunset['data']['timelines'][0]['intervals'][0]['startTime'], "%Y-%m-%dT%H:%M:%S%z")
offset = tmp.utcoffset().total_seconds()/3600.

sunsets = []
sunrises = []
moonsets = []
moonrises = []
ccTups = []

for elem in sunset['data']['timelines'][0]['intervals']:
    #each elem is a dictionary with startTime and values Dict with moonPhase, moonriseTime, moonsetTime, sunriseTime, sunsetTime
    values = elem['values']
    
    sunsetTime = (datetime.strptime(values['sunsetTime'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=offset))
    sunriseTime = (datetime.strptime(values['sunriseTime'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=offset))
    moonsetTime = (None if values['moonsetTime'] == None else (datetime.strptime(values['moonsetTime'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=offset)))
    moonriseTime = (None if values['moonriseTime'] == None else(datetime.strptime(values['moonriseTime'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=offset)))

    sunsets.append((hour_rounder(sunsetTime).strftime("%Y%m%dT%H%M %a"),"ss{}".format(sunsetTime.strftime("%H%M"))))
    sunrises.append((hour_rounder(sunriseTime).strftime("%Y%m%dT%H%M %a"),"sr{}".format(sunriseTime.strftime("%H%M"))))
    try:
        moonsets.append((hour_rounder(moonsetTime).strftime("%Y%m%dT%H%M %a"),"ms{}".format(moonsetTime.strftime("%H%M"))))
    except AttributeError:
        pass

    try:
        moonrises.append((hour_rounder(moonriseTime).strftime("%Y%m%dT%H%M %a"),"mr({}){}".format(moonPhase[values['moonPhase']],moonriseTime.strftime("%H%M"))))    
    except AttributeError:
        pass

for elem in cc['data']['timelines'][0]['intervals']:
    startTime = datetime.strptime(elem['startTime'], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y%m%dT%H%M %a")
    cCov = int(elem['values']['cloudCover'])
    ccTups.append((startTime, "tCC:{:03d}".format(cCov)))


#Mush all other info onto NOAA Tups
## Define a lambda function to grab just the first element for comparisons
y = lambda x: x[0]
idinfo = {y(rec): rec[1:] for rec in ccTups}  # Dict for fast look-ups.
merged = [info + idinfo[y(info)] for info in nccTups if y(info) in idinfo]
print(len(merged))

idinfo = {y(rec): rec[1:] for rec in sunsets}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]

merged = sorted(list(set(merged + tmp)))
print(len(merged))

idinfo = {y(rec): rec[1:] for rec in sunrises}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]

merged = sorted(list(set(merged + tmp)))
print(len(merged))

idinfo = {y(rec): rec[1:] for rec in moonrises}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]

merged = sorted(list(set(merged + tmp)))
print(len(merged))

idinfo = {y(rec): rec[1:] for rec in moonsets}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]

merged = sorted(list(set(merged + tmp)))
print(len(merged))

final = [merged[0]]
for i in range(1,len(merged)):
    if merged[i][:3] == merged[i-1][:3]:
        continue
    else:
        final.append(merged[i-1])

print(len(final))
for elem in final:
    print(elem)