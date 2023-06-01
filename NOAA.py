import xmltodict
import os
from datetime import datetime, timedelta



def generateNOAATuples():
    url = "https://forecast.weather.gov/MapClick.php?lat=39.2906&lon=-76.6093&FcstType=digitalDWML"

    os.system("curl \"{}\" > noaa.xml 2> /dev/null".format(url))

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
    
    return nccTups