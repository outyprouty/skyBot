import xmltodict
from datetime import datetime
#url = "https://forecast.weather.gov/MapClick.php?lat=39.2906&lon=-76.6093&FcstType=digitalDWML"

#os.system("curl \"{}\" > noaa.xml".format(url))

xmlData = open("noaa.xml", 'r').read()
data = xmltodict.parse(xmlData)

hrs=data['dwml']['data']['time-layout']['start-valid-time']

ccs=data['dwml']['data']['parameters']['cloud-amount']['value']

ccTups = []

for time,cc in zip(hrs, ccs):
    dtime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
    ccTups.append((dtime.strftime("%a %Y%m%dT%H%M"),"nCC:{:03d}".format(int(cc)) ))

print(ccTups)