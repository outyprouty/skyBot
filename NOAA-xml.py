import xmltodict
import os

#url = "https://forecast.weather.gov/MapClick.php?lat=39.2906&lon=-76.6093&FcstType=digitalDWML"

#os.system("curl \"{}\" > noaa.xml".format(url))


xmlData = open("noaa.xml", 'r').read()
data = xmltodict.parse(xmlData)

print(data['dwml']['data']['time-layout']['start-valid-time'])

print(data['dwml']['data']['parameters']['cloud-amount']['value'])

print(data['dwml']['data'].keys())