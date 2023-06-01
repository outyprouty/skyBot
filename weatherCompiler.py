import xmltodict, requests
from datetime import datetime
import dotenv, os
from datetime import datetime, timedelta
import json
import pytz
import sys

dotenv.load_dotenv()

from NOAA import generateNOAATuples
nccTups = generateNOAATuples(verbose=False)

from tomorrow import generateSunMoonTuples, generateCloudCoverTuples
sunsets, sunrises, moonsets, moonrises = generateSunMoonTuples(verbose=True)
ccTups = generateCloudCoverTuples(verbose=False)

#Mush all other info onto NOAA Tups
## Define a lambda function to grab just the first element for comparisons
y = lambda x: x[0]

idinfo = {y(rec): rec[1:] for rec in ccTups}  
merged = [info + idinfo[y(info)] for info in nccTups if y(info) in idinfo]

idinfo = {y(rec): rec[1:] for rec in sunsets}  
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

idinfo = {y(rec): rec[1:] for rec in sunrises}  
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

idinfo = {y(rec): rec[1:] for rec in moonrises}  
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

idinfo = {y(rec): rec[1:] for rec in moonsets}  
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

final = [merged[0]]
for i in range(1,len(merged)):
    if merged[i][:3] == merged[i-1][:3]:
        continue
    else:
        final.append(merged[i-1])

## Print listing so far
for elem in final:
    print(elem)

## Generate a new list with a ranking appended



