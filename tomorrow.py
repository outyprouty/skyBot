import xmltodict, requests
from datetime import datetime
import dotenv, os
from datetime import datetime, timedelta
import json
import pytz
import sys

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


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    if t == None:
        return None
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))



dotenv.load_dotenv()

## Get sunset data
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
sunset.replace('null', "None") #Moonrise/setTimes can be 'null' in time interval
sunset=json.loads(sunset)

## Get cloud cover data
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
cc=json.loads(response.text)

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
