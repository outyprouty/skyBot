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
sunMoonFile = "sunMoon.json"
cloudCoverFile = "cloudCover.json"


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    if t == None:
        return None
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))


def getSunMoonData(verbose=False):
    try:
        if verbose: print("Want to see if sunMoon file exists")
        with open(sunMoonFile, 'r') as f:
            lastWritten = f.read(13)
            if verbose: print("File exists, found last write date as", lastWritten)
            if (datetime.now() - timedelta(hours=3)) < datetime.strptime(lastWritten, "%Y%m%dT%H%M"):
                #The file is NEW
                sunMoon=json.loads(f.read())
                return sunMoon
            if verbose: print("File found, but too old, generating new one")

    except FileNotFoundError:
        if verbose: print("Could not find file")
        pass


    #No recent file could be found, so we're generating it now
    querystring = {
    "location":"6477cc2713627de22c3eb131",
    "fields":["sunsetTime", "sunriseTime", "moonPhase", "moonriseTime", "moonsetTime"],
    "timesteps":"1d",
    ## TODO: Roy figure out why tommorrowAPI complains about this code generating dates in the past
    #"startTime":datetime.now().strftime("%Y-%m-%d"),
    #"endTime":(datetime.now()+timedelta(days=3)).strftime("%Y-%m-%d"),
    "timezone":"America/New_York",
    "apikey":os.getenv("tomorrowAPIKey")}

    response = requests.request("GET", url, params=querystring)
    sunMoon=response.text
    sunMoon.replace('null', "None") #Moonrise/setTimes can be 'null' in time interval
    with open(sunMoonFile, 'w') as f:
        f.write(datetime.now().strftime("%Y%m%dT%H%M"))
        f.write(sunMoon)
        if verbose: print("Got API data, wrote to file.")

    sunMoon=json.loads(sunMoon)
    return sunMoon

def generateSunMoonTuples(verbose=False):
    sunsets, sunrises, moonsets, moonrises = [], [], [], []

    sunMoon = getSunMoonData(verbose=verbose)
    if verbose: print("Tomorrow API Raw SunMoon Data\n",sunMoon)

    tmp = datetime.strptime(sunMoon['data']['timelines'][0]['intervals'][0]['startTime'], "%Y-%m-%dT%H:%M:%S%z")
    offset = tmp.utcoffset().total_seconds()/3600.

    for elem in sunMoon['data']['timelines'][0]['intervals']:
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
    if verbose: print("Sunsets\n",sunsets,"\nSunrises\n", sunrises, "\nMoonsets\n", moonsets, "Moonrises", moonrises)
    return sunsets, sunrises, moonsets, moonrises

def getCloudCoverData(verbose=False):
    try:
        if verbose: print("Want to see if cloudCover file exists")
        with open(cloudCoverFile, 'r') as f:
            lastWritten = f.read(13)
            if verbose: print("File exists, found last write date as", lastWritten)
            if (datetime.now() - timedelta(hours=3)) < datetime.strptime(lastWritten, "%Y%m%dT%H%M"):
                #The file is NEW
                cloudCov=json.loads(f.read())
                return cloudCov
            if verbose: print("File found, but too old, generating new one")
    except FileNotFoundError:
        if verbose: print("Could not find file")
        pass


    ## Get cloud cover data
    querystring = {
    "location":"6477cc2713627de22c3eb131",
    "fields":["cloudCover"],
    "units":"metric",
    ## TODO: Roy figure out why tommorrowAPI complains about this code generating dates in the past
    #"startTime":datetime.now().strftime("%Y-%m-%d"),
    #"endTime":(datetime.now()+timedelta(days=3)).strftime("%Y-%m-%d"),
    "timesteps":"1h",
    "timezone":"America/New_York",
    "apikey":os.getenv("tomorrowAPIKey")}

    response = requests.request("GET", url, params=querystring)
    cloudCov=response.text
    with open(cloudCoverFile, 'w') as f:
        f.write(datetime.now().strftime("%Y%m%dT%H%M"))
        f.write(cloudCov)
        if verbose: print("Got API data, wrote to file.")

    cloudCov=json.loads(cloudCov)
    return cloudCov

def generateCloudCoverTuples(verbose=False):
    cCovTups = []
    
    cloudCov = getCloudCoverData(verbose=verbose)
    if verbose: print("Tomorrow API Raw Cloud Coverage\n",cloudCov)

    for elem in cloudCov['data']['timelines'][0]['intervals']:
        startTime = datetime.strptime(elem['startTime'], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y%m%dT%H%M %a")
        cCovPercentage = int(elem['values']['cloudCover'])
        cCovTups.append((startTime, "tCC:{:03d}".format(cCovPercentage)))

    if verbose: print("Tomorrow Cloud Coverage Tuples\n",cCovTups)
    return cCovTups