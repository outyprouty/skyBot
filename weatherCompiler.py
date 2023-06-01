import xmltodict, requests
from datetime import datetime
import dotenv, os
from datetime import datetime, timedelta
import json
import pytz
import sys





from NOAA import generateNOAATuples

nccTups = generateNOAATuples()



#######


#Mush all other info onto NOAA Tups
## Define a lambda function to grab just the first element for comparisons
y = lambda x: x[0]
idinfo = {y(rec): rec[1:] for rec in ccTups}  # Dict for fast look-ups.
merged = [info + idinfo[y(info)] for info in nccTups if y(info) in idinfo]

idinfo = {y(rec): rec[1:] for rec in sunsets}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

idinfo = {y(rec): rec[1:] for rec in sunrises}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

idinfo = {y(rec): rec[1:] for rec in moonrises}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))

idinfo = {y(rec): rec[1:] for rec in moonsets}  # Dict for fast look-ups.
tmp = [info + idinfo[y(info)] for info in merged if y(info) in idinfo]
merged = sorted(list(set(merged + tmp)))


final = [merged[0]]
for i in range(1,len(merged)):
    if merged[i][:3] == merged[i-1][:3]:
        continue
    else:
        final.append(merged[i-1])


for elem in final:
    print(elem)

