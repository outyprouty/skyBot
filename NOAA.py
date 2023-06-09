import xmltodict
import os
from datetime import datetime


def generateNOAATuples(verbose=False):
    #url = "https://forecast.weather.gov/MapClick.php?lat=39.2906&lon=-76.6093&FcstType=digitalDWML"
    url = "https://forecast.weather.gov/MapClick.php?lat={:0.4f}&lon={:0.4f}&FcstType=digitalDWML".format(float(os.getenv("LAT")), float(os.getenv("LON")))
    print(url)

    os.system("curl \"{}\" > noaa.xml 2> /dev/null".format(url))

    xmlData = open("noaa.xml", 'r').read()
    data = xmltodict.parse(xmlData)
    if verbose: print("NOAA Data\n",data)
    hrs=data['dwml']['data']['time-layout']['start-valid-time']

    ccs=data['dwml']['data']['parameters']['cloud-amount']['value']

    nccTups = []

    for time,cc in zip(hrs, ccs):
        dtime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        try:
            nccTups.append((dtime.strftime("%Y%m%dT%H%M %a"),"nCC:{:03d}".format(int(cc)) ))
        except TypeError:
            continue
    if verbose: print("NOAA Tuples\n", nccTups)
    return nccTups