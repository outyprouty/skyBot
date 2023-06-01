import dotenv
from datetime import datetime

class WeatherCompiler:

    def __init__(self):
        dotenv.load_dotenv()

        from NOAA import generateNOAATuples
        nccTups = generateNOAATuples(verbose=False)

        from tomorrow import generateSunMoonTuples, generateCloudCoverTuples
        sunsets, sunrises, moonsets, moonrises = generateSunMoonTuples(verbose=False)
        ccTups = generateCloudCoverTuples(verbose=False)

        #Rolling avg window
        N = 2

        #score threshold
        self.thresh = 0.3

        #number of days out to report on
        self.outlook = 3

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
                if final[-1] != merged[i-1]:
                    final.append(merged[i-1])
                
        ## Generate a new list with a ranking appended
        rankings = [[-1, *e] for e in final]

        #Cycle once to find dark hours
        dark = False
        for r in rankings:
            weight = 1
            if len(r) > 4:
                if 'sr' in r[4]:
                    dark = False
                if 'ss' in r[4]:
                    dark = True
                    weight = N # This is to avoid sunsets being poorly weighted
            else:
                pass
            r[0] = weight if dark else 0

        #Cycle again and apply formula for cloud cover
        cloudRank = lambda n, t: (100-n)*(100-t)/10000.
        for r in rankings:
            ncc = int(r[2].split(':')[1])
            tcc = int(r[3].split(':')[1])
            r[0] = cloudRank(ncc, tcc)*r[0]

        #Cycle ONCE MORE applying an N-hr rolling average
        for i in range(N-1, len(rankings)):
            avg = sum([rankings[j][0] for j in range(i-N+1, i+1)])
            rankings[i][0] = float(avg)/N if rankings[i][0] > 0 else 0

        # Effectively -1-out the first N entries, since they won't have 
        #  scores on the same basis
        for i in range(0,N):
            rankings[i][0] = -1

        #Write the report to file
        with open("report.txt", 'w') as f:
            for r in rankings:
                f.write("{:0.2f}".format(r[0]))
                for e in r[1:]:
                    f.write(",{}".format(e))
                f.write("\n")

        self.reportFile = "report.txt"
        self.report = [f.strip().split(',') for f in open("report.txt").readlines()]

        self.getDays()

    def getDays(self):
        days = []
        dates = [line[1] for line in self.report]
        uniqueDates = sorted(list(set([datetime.strptime(l, "%Y%m%dT%H%M %a").date() for l in dates])))
        
        #doens't scale well, but dataset is small by definition, SO WHO CARES
        for uDay in uniqueDates:
            tmp = []
            for d in self.report:
                if uDay == datetime.strptime(d[1], "%Y%m%dT%H%M %a").date():
                    tmp.append(d)
            days.append(Day(uDay, tmp))
        self.days = days

    def getDetails(self):
        detailStr = ""
        for day in self.days[:self.outlook]:
            detailStr += day.date.strftime("%a %Y%m%d") + "\n"
            for d in day.dayLines:
                if float(d[0]) == -1.0:
                    continue
                detailStr += "  Score {:04.2f} {} Avg CCov: {:03d} % \n".format(\
                    float(d[0]), datetime.strptime(d[1], "%Y%m%dT%H%M %a").strftime("%H:00"), \
                    int(0.5*(float(d[2].split(':')[1]) + float(d[3].split(':')[1]))))
        return detailStr
    
    def getSummary(self):
        summaryStr = ""
        for day in self.days[:self.outlook]:
            sunrise = "Not in range" if day.sunrise == None else day.sunrise.strftime("%H%M") 
            sunset = "Not in range" if day.sunset == None else day.sunset.strftime("%H%M") 
            moonrise = "Not in range" if day.moonrise == None else day.moonrise.strftime("%H%M") 
            moonphase = day.moonphase
            moonset = "Not in range" if day.moonset == None else day.moonset.strftime("%H%M") 
            
            summaryStr += \
"""
{}
Sunrise: {}
Sunset: {}
Moonrise: {} ({})
Moonset: {}
Number of Dark Hrs Before/After Sunrise/set: {}/{}
\n""".format(day.date.strftime("%a %Y%m%d"), sunrise, sunset, moonrise, moonphase, moonset, *self.getDarkHrs(day))
        return summaryStr
    
    def getDarkHrs(self, day):
        beforeSR, afterSS = 0, 0
        if day.sunrise == None: beforeSR = -1
        if day.sunset == None: afterSS = -1
        for d in day.dayLines:
            if float(d[0]) > self.thresh:
                if beforeSR != -1: 
                    if datetime.strptime(d[1], "%Y%m%dT%H%M %a").hour <= day.sunrise.hour: 
                        beforeSR += 1
                if afterSS != -1: 
                    if datetime.strptime(d[1], "%Y%m%dT%H%M %a").hour >= day.sunset.hour: 
                        afterSS += 1

        return beforeSR, afterSS
    def getHelp(self):
        return """
General: `skyBot` uses NOAA and TomorrowAPI to gather some sky data and 
    organize it for 'easy' viewing.

Usage: `skyBot summary | details | help`

`summary`: Gives three-day sun/moon information along with estimates of
    number of hours before and after sunset with clear skies
`details`: Gives three-day 'score' (see below) for each hour along with averge of
    NOAA and Tomorrow API cloud cover forecast.

What does 'clear' mean? NOAA and Tomorrow API agree forecast less 
    than 30\% cloud cover while dark over a three-hour rolling window
    centered on the hour in question.
"""


class Day:

    def __init__(self, date, dayLines):
        self.dayLines = dayLines
        self.date = date
        self.sunrise = self.findSunrise()
        self.sunset = self.findSunset()
        self.moonrise, self.moonphase = self.findMoonrise()
        self.moonset = self.findMoonset()

    def findSunrise(self):
        for d in self.dayLines:
            if len(d) > 4:
                if 'sr' in d[4]:
                    return datetime.strptime(self.date.strftime("%Y%m%dT")+d[4][2:], "%Y%m%dT%H%M")
        return None
    
    def findSunset(self):
        for d in self.dayLines:
            if len(d) > 4:
                if 'ss' in d[4]:
                    return datetime.strptime(self.date.strftime("%Y%m%dT")+d[4][2:], "%Y%m%dT%H%M")
        return None
    
    def findMoonrise(self):
        for d in self.dayLines:
            if len(d) > 4:
                if 'mr' in d[4]:
                    return datetime.strptime(self.date.strftime("%Y%m%dT")+d[4][-2:], "%Y%m%dT%H%M"), d[4].split('(')[1].split(')')[0]
        return None, None
    
    def findMoonset(self):
        for d in self.dayLines:
            if len(d) > 4:
                if 'ms' in d[4]:
                    return datetime.strptime(self.date.strftime("%Y%m%dT")+d[4][2:], "%Y%m%dT%H%M")
        return None

if __name__ == "__main__":
    wc = WeatherCompiler()
    print(wc.getSummary())
    print()
    print(wc.getDetails())

