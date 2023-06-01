import dotenv

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
        thresh = 0.3

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

        for i in range(0,N):
            rankings[i][0] = -1

        with open("report.txt", 'w') as f:
            for r in rankings:
                f.write("{:0.2f} {}\n".format(r[0], r[1:]))

        self.reportFile = "report.txt"
        self.report = [f.strip() for f in open("report.txt").readlines()]

    def getDays(self):
        days = list(set([line.split()[1] for line in self.report]))
        print(days)

wc = WeatherCompiler()
    
wc.getDays()


