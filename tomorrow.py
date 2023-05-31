import requests
import dotenv, os
from datetime import datetime, timedelta
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

# weekdays = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]

class TomorrowParser:

    def __init__(self):
        UTC_OFFSET = -1
        dotenv.load_dotenv()

        #Get sunset data
        # querystring = {
        # "location":"6477cc2713627de22c3eb131",
        # "fields":["sunsetTime", "sunriseTime", "moonPhase"],
        # "timesteps":"1d",
        # "timezone":"America/New_York",
        # "apikey":os.getenv("tomorrowAPIKey")}

        # response = requests.request("GET", url, params=querystring)
        # print(response.text)
        self.sunset={"data":{"timelines":[{"timestep":"1d","endTime":"2023-06-05T06:00:00-04:00","startTime":"2023-05-31T06:00:00-04:00","intervals":[{"startTime":"2023-05-31T06:00:00-04:00","values":{"moonPhase":3,"sunriseTime":"2023-05-31T09:54:00Z","sunsetTime":"2023-06-01T00:14:00Z"}},{"startTime":"2023-06-01T06:00:00-04:00","values":{"moonPhase":3,"sunriseTime":"2023-06-01T09:54:00Z","sunsetTime":"2023-06-02T00:15:00Z"}},{"startTime":"2023-06-02T06:00:00-04:00","values":{"moonPhase":3,"sunriseTime":"2023-06-02T09:54:00Z","sunsetTime":"2023-06-03T00:15:00Z"}},{"startTime":"2023-06-03T06:00:00-04:00","values":{"moonPhase":4,"sunriseTime":"2023-06-03T09:54:00Z","sunsetTime":"2023-06-04T00:15:00Z"}},{"startTime":"2023-06-04T06:00:00-04:00","values":{"moonPhase":4,"sunriseTime":"2023-06-04T09:54:00Z","sunsetTime":"2023-06-05T00:16:00Z"}},{"startTime":"2023-06-05T06:00:00-04:00","values":{"moonPhase":4,"sunriseTime":"2023-06-05T09:54:00Z","sunsetTime":"2023-06-06T00:16:00Z"}}]}]}}

        #Get cloud cover data
        # querystring = {
        # "location":"6477cc2713627de22c3eb131",
        # "fields":["cloudCover"],
        # "units":"metric",
        # "timesteps":"1d",
        # "timezone":"America/New_York",
        # "apikey":os.getenv("tomorrowAPIKey")}

        # response = requests.request("GET", url, params=querystring)
        # print(response.text)
        self.cc={"data":{"timelines":[{"timestep":"1d","endTime":"2023-06-05T06:00:00-04:00","startTime":"2023-05-31T06:00:00-04:00",\
                        "intervals":[{"startTime":"2023-05-31T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-01T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-02T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-03T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-04T06:00:00-04:00","values":{"cloudCover":100}},{"startTime":"2023-06-05T06:00:00-04:00","values":{"cloudCover":100}}]}]}}
        




def startTimeToLocal(dateString, timeOnly=False):
    UTC_DELTA=int(dateString.split('-')[-1].split(':')[0])
    
    localDateTime = datetime.strptime(dateString.split('-')[:-1], "%Y-%m-%dT%H:%M:%S") + timedelta(hours=UTC_DELTA)
    if timeOnly:
        return localDateTime.strftime("%a %H%M")
    else:
        return localDateTime.strftime("%a %Y%m%dT%H%M")


intervals = sunset['data']['timelines'][0]['intervals']

for dayNum in range(len(intervals)):
    string = \
"""
{}
Sunset: {}
Sunrise: {}
""".format(startTimeToLocal(intervals[dayNum]['startTime']), \
           getDateFromUTC(intervals[dayNum]['sunsetTime'], True), \
           getDateFromUTC(intervals[dayNum]['sunriseTime']))
    print(string)
    










