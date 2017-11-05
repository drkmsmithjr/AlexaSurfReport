
"""
SurfReport

#Written by Mark Smith, www.surfncircuits.com

 Class Surfspot uses the 
# Surfline API Report Parser 
# modified by Mark Smith
# www.surfncircuit.com
# Used surfMax and surfMin from spot report and regional report 
# added SurfText inputs.    

# Based on Code Written by Colin Karpfinger
# http://punchthrough.com/bean/examples/surf-report-notifier/
# copyright (c) 2014 Punch Through Design

"""

import datetime
import urllib2
import json
import time
from decimal import *
import string


# defining the surf spots
# first number: SurlineID spot
# second number: surfline Regional Spot
# third number: NOAA tide ID location

spots = {
    'uppers':["4738","2950","TWC0419"],
    'upper trestles':["4738","2950","TWC0419"],
    'upper':["4738","2950","TWC0419"],
    'salt creek':["4233","2950","TWC0419"],
    'doheny':["4848","2950","TWC0419"],
    'doheny state beach':["4848","2950","TWC0419"],
    'lowers':["4740","2950","TWC0419"],
    'lower trestles':["4740","2950","TWC0419"],
    'lower':["4740","2950","TWC0419"],
    't-street':["4235","2950","TWC0419"],
    'T. street' :["4235","2950","TWC0419"],
    'san clementi state beach':["4843","2950","TWC0419"],
    'the point':["4237","2950","TWC0419"],
    'old mans':["109918","2950","TWC0419"],
    'hb pier':["4874","2143","9410580"],
    'HB pier':["4874","2143","9410580"],
    'h. b. pier':["4874","2143","9410580"],
    'Huntington beach pier':["4874","2143","9410580"],
    '56th street':["43103","2143","9410580"],
    'fifty sixth street':["43103","2143","9410580"],
    'the wedge':["4232","2143","9410580"],
    'goldenwest':["4870","2143","9410580"],
    'golden west':["4870","2143","9410580"],
    'huntington state beach':["103681","2143","9410580"],
    'Huntington state beach':["103681","2143","9410580"],
    'seal beach':["4217","2143","9410580"],
    'bolsa chica':["4868","2143","9410580"],
    'bolsa chica state beach':["4868","2143","9410580"],
    'Newport point':["4877","2143","9410580"],
    'blackies':["53412","2143","9410580"],    
    'oceanside harbor':["4238","2144","TWC0419"],
    'oceanside pier south side':["4241","2144","TWC0419"],
    'oceanside pier north side':["68366","2144","TWC0419"]
    
}

daysInReport = 6
conditionTypes=["","flat", "very poor", "poor","poor to fair","fair","fair to good","good","very good","good to epic","epic"]

# to account for the Server Location in Ireland
hourcorrection = datetime.timedelta(hours = 6)

class SurfSpot:
    baseUrl="http://api.surfline.com/v1/forecasts/0000?resources=surf,analysis&days=6&getAllSpots=false&units=e&interpolate=false&showOptimal=false"
    
    # ZZZZZZZZ equals YEAR 4 characters, MOnth 2 characters, Day 2 characters
    # YYYYYYYY equals YEAR 4 characters, month 2 characters, day 2 charactors
    # XXXXXXX is from the NOAA station number.  Some stations need testing to be sure    
    baseUrlNoaa="https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=ZZZZZZZZ&end_date=YYYYYYYY&datum=MLLW&station=XXXXXXX&time_zone=lst_ldt&units=english&interval=hilo&format=json"
    heightsMax=[]
    heightsMin=[]

    surflineUrl=""
    tideUrl=""
    surflineRegionalUrl=""
    surflineName=""
    textConditions=[]
    spotName =""
    todaysLocalCondition=0
    regionalConditions=[]
    Tides=[]
    
    def __init__(self, spotName, spotID, regionalID, tideID):
        # create object with the spot name, spotID and regionalID.  Both are available in HTTP addresss associaed with  
        # the surfline.com site.    
        self.spotName = spotName
        self.surflineUrl=self.baseUrl.replace("0000",spotID)
        self.surflineRegionalUrl=self.baseUrl.replace("0000",regionalID)
        
        # get today's datetime and x days ahead to find all tide swings between days
        now = datetime.date.today()
        #print(now.strftime("%Y%m%d"))
        dayssix = datetime.timedelta(days = daysInReport)
        nowdayssix = now+dayssix
        #print(nowdayssix.strftime("%Y%m%d"))
        
        self.noaaTideUrl=self.baseUrlNoaa.replace("XXXXXXX",tideID)
        self.noaaTideUrl=self.noaaTideUrl.replace("ZZZZZZZZ",now.strftime("%Y%m%d"))
        self.noaaTideUrl=self.noaaTideUrl.replace("YYYYYYYY",nowdayssix.strftime("%Y%m%d"))

        #print(self.noaaTideUrl)
        # all these arrays can have totals each day        
        self.heightsMax=[]
        self.heightsMin=[]
        self.surfText=[]
        self.regionalConditions=[]
        
        # high tides time for each day.   The items of each day will be another arrays
        # the array items will be array for each day.  = [tidetime1,tidetime2]
        # we will keep track of tides during day +- 1 hours before after sunset.
        self.hightidetimes=[]
        self.lowtidetimes=[]
        self.hightidevalues= []
        self.lowtidevalues=[]
        
        # for the day, we need the next tide value and time
        self.nexttidetime = datetime.date.today()
        self.nexttidevalue = 1
        self.nexttimetype = "HIGH"   
        
        # default best day to surf is today
        self.bestdaytosurf = 0
        
        
    def parseTideReport(self,tideReport):
    
        hightidetimes = []
        hightidevalues = []
        lowtidetimes = []
        lowtidevalues = []        

        HT = []
        HTV = []
        LT = []
        LTV = []
                     
        # parse the tidereport and put it into hightide,lowtide arrayrs 
        #print("inside Parse Tide Report")    
        #print(tideReport)
        # parse all the high tides and low times and values       
        for t in range(len(tideReport["predictions"])):
           if tideReport["predictions"][t]["type"]=="H":
              hightidetimes.append(tideReport["predictions"][t]["t"])
              hightidevalues.append(tideReport["predictions"][t]["v"])
           else:
              lowtidetimes.append(tideReport["predictions"][t]["t"])
              lowtidevalues.append(tideReport["predictions"][t]["v"])
        # now parse these lists into smaller arrays of days for each day
        day = 0
        indexdate = datetime.date.today()
        daydelta = datetime.timedelta(days = 1)    
        for t in range(len(hightidetimes)):
        # convert this into a date time object
           tidetime = datetime.datetime.strptime(hightidetimes[t], "%Y-%m-%d %H:%M")
           #print(tidetime)
           #print(indexdate)
           if tidetime.day == indexdate.day:
              HT.append(tidetime.strftime("%I:%M %p"))
              HTV.append(hightidevalues[t])
           else:
              #save the current day 
              #print(tidetime.day)
              #print(indexdate.day)              
              self.hightidetimes.append(HT)
              self.hightidevalues.append(HTV)
              #reset the array
              HT = []
              HTV = []
              #save the current tidetime into a new array
              HT.append(tidetime.strftime("%I:%M %p"))
              HTV.append(hightidevalues[t])
              # update the index time              
              day = day +1
              indexdate = indexdate + daydelta
            # save the last day array.   
           if t==len(hightidetimes)-1:
              self.hightidetimes.append(HT)
              self.hightidevalues.append(HTV)            
                            
        #print(hightidetimes)
        #print("\n")
        #print(hightidevalues)
        #print(lowtidetimes)
        #print(lowtidevalues)
        #print(self.hightidetimes)
        #print(self.hightidevalues)
        
        # now parse the low tide lists into smaller arrays of days.
        day = 0
        indexdate = datetime.date.today()
        daydelta = datetime.timedelta(days = 1)    
        for t in range(len(lowtidetimes)):
        # convert this into a date time object
           tidetime = datetime.datetime.strptime(lowtidetimes[t], "%Y-%m-%d %H:%M")
           #print(tidetime)
           #print(indexdate)
           if tidetime.day == indexdate.day:
              LT.append(tidetime.strftime("%I:%M %p"))
              LTV.append(lowtidevalues[t])
           else:
              #save the current day 
              #print(tidetime.day)
              #print(indexdate.day)              
              self.lowtidetimes.append(LT)
              self.lowtidevalues.append(LTV)
              #reset the array
              LT = []
              LTV = []
              #save the current tidetime into a new array
              LT.append(tidetime.strftime("%I:%M %p"))
              LTV.append(lowtidevalues[t])
              # update the index time              
              day = day +1
              indexdate = indexdate + daydelta
            # save the last day array.   
           if t==len(lowtidetimes)-1:
              self.lowtidetimes.append(LT)
              self.lowtidevalues.append(LTV)            
        #print(lowtidetimes)
        #print("\n")
        #print(lowtidevalues)
        #print(lowtidetimes)
        #print(lowtidevalues)
        #print(self.lowtidetimes)
        #print(self.lowtidevalues)
          
        # need to find out the next tide and and value
        nowtime = datetime.datetime.now() - hourcorrection
        
        for t in range(len(tideReport["predictions"])):
           tidetime = datetime.datetime.strptime(tideReport["predictions"][t]["t"], "%Y-%m-%d %H:%M")
           if tidetime > nowtime:
              self.nexttidetime = tidetime.strftime("%I:%M %p")
              self.nexttidevalue = tideReport["predictions"][t]["v"]
              if tideReport["predictions"][t]["type"]=="H":
                 self.nexttimetype = "HIGH"
              else:
                 self.nexttimetype = "LOW"               
              break
        #if self.nexttimetype == "HIGH":
        #   print("the side is rising to a value of ")
        #else:
           #print("the tide will be falling to a value of ")   
        #print(self.nexttidevalue)
        #print("at time:")
        #print(self.nexttidetime)
                
    def getTideReport(self):       
        webreq = urllib2.Request(self.noaaTideUrl, None, {'user-agent':'www.surfncircuits.com'})
        f = urllib2.urlopen(webreq)
        fstr = f.read()
        #print fstr
        tideReport=json.loads(fstr)
        #print tideReport["predictions"][0]["type"]                           
        # get tide information 
        self.parseTideReport(tideReport)  
           
                
    def getReport(self):
        # use the spot API to get the current information
        # use the regional API address (regionsalReport) to get the forecast information
        # uses the NOAA datagetter https://tidesandcurrents.noaa.gov/api/datagetter?
        
        webreq = urllib2.Request(self.surflineUrl, None, {'user-agent':'www.surfncircuits.com'})
        f = urllib2.urlopen(webreq)
        fstr = f.read()
        fstr = fstr.replace(')','') #remove closing )
        fstr = fstr.replace(';','') #remove semicolon
        fstr = fstr.strip() #remove any whitespace in start/end
        rep = json.loads(fstr)
        

        webreq = urllib2.Request(self.surflineRegionalUrl, None, {'user-agent':'www.surfncircuits.com'})
        #print 'request method :',webreq.get_method()
        #opener = urllib2.build_opener()
        #f = opener.open(webreq)
        f = urllib2.urlopen(webreq)
        fstr = f.read()
        fstr = fstr.replace(')','') #remove closing )
        fstr = fstr.replace(';','') #remove semicolon
        fstr = fstr.strip() #rem3ove any whitespace in start/end
        regionalReport=json.loads(fstr)

        # save the surf report for each day
        self.surflineName=rep["name"]
        for day in range(0,daysInReport):
            daysAvgMax=0
            daysAvgMin=0
            self.regionalConditions.append(conditionTypes.index(regionalReport["Analysis"]["generalCondition"][day]))
            if day == 0:
               if ((len(rep["Analysis"]["surfMax"]) > 0) and (rep["Analysis"]["surfMax"][day] != "")) :
                  daysAvgMax=rep["Analysis"]["surfMax"][day]
                  daysAvgMin=rep["Analysis"]["surfMin"][day]
                  self.surfText.append(rep["Analysis"]["surfText"][day])
               else:
                  daysAvgMax=regionalReport["Analysis"]["surfMax"][day]
                  daysAvgMin=regionalReport["Analysis"]["surfMin"][day]
                  self.surfText.append(regionalReport["Analysis"]["surfText"][day])
            else:
               daysAvgMax=regionalReport["Analysis"]["surfMax"][day]
               daysAvgMin=regionalReport["Analysis"]["surfMin"][day]
               self.surfText.append(regionalReport["Analysis"]["surfText"][day])
                                
 #           self.heightsMax.append(Decimal(daysAvgMax).quantize(Decimal('1'), rounding=ROUND_UP))
 #           self.heightsMin.append(Decimal(daysAvgMin).quantize(Decimal('1'), rounding=ROUND_UP))
            self.heightsMax.append(daysAvgMax)
            self.heightsMin.append(daysAvgMin)
            
        self.bestdaysearch()
    
    def bestdaysearch(self):
    # search for the best day to surf
    # criteria:   Highest surf the soonest
       bestday = 0
       for day in range(0,daysInReport):
          bestdayaveheight = (self.heightsMax[bestday]+self.heightsMin[bestday])/2.0
          #print(bestdayaveheight)
          indexdayaveheight = (self.heightsMax[day]+self.heightsMin[day])/2.0
          #print(indexdayaveheight)
          if indexdayaveheight > bestdayaveheight:
             bestday = day
       self.bestdaytosurf = bestday
       #print(self.bestdaytosurf)
       #print(self.heightsMax)
       #print(self.heightsMin)
             
    def printReport(self, day = None):
    # print the day in the report. day 1 is current day
    # when no day is present just show all days in forecast  
        reportText=self.spotName+" is "
        if day == None:
            for day in range(0,daysInReport):
                reportText=reportText+str(self.heightsMin[day])+"-"+str(self.heightsMax[day])+" ft. "+str(conditionTypes[self.regionalConditions[day]])+"  " + str(self.surfText[day])+"  "
        else:
            if day >= daysInReport:
                day = daysInReport - 1
            reportText=reportText+str(self.heightsMin[day])+"-"+str(self.heightsMax[day])+" ft. "+str(conditionTypes[self.regionalConditions[day]])+"  " + str(self.surfText[day])+"  "
        #reportText = reportText + "\n"    
        #print reportText
        return reportText
          
    def printTideReport(self,day = None):
        reportText = ""
        tidetext = ""
        if day == 0:
           reportText = "The tide for " + self.spotName + " is "
           if self.nexttimetype == "HIGH":
              reportText = reportText + "rising to a high of "
           else:
              reportText = reportText + "falling to a low of "
           reportText = reportText + str(round(float(self.nexttidevalue),1)) + " at "
           reportText = reportText + str(self.nexttidetime) + ".           "
        else:
           if len(self.hightidetimes)>1:
              tidetext = " There are high Tides at "
           else:
              tidetext = "There is a high Tides at "
           for x in range(0,len(self.hightidetimes[day])):
              tidetext = tidetext + self.hightidetimes[day][x]
              if x != len(self.hightidetimes[day])-1:
                 tidetext = tidetext + " and "
              else:
                 tidetext = tidetext + ".   "
           if len(self.hightidetimes)>1:
              tidetext = tidetext + " The tide values are  "
           else:
              tidetext = tidetext + " The tide value is "
           for x in range(0,len(self.hightidetimes[day])):
              tidevalue = round(float(self.hightidevalues[day][x]),1)
              #print(round(float(tidevalue),1))
              tidetext = tidetext + str(tidevalue)
              if x != len(self.hightidetimes[day])-1:
                 tidetext = tidetext + " and "
              else:
                 tidetext = tidetext + " feet.        "
                 
           if len(self.hightidetimes)>1:
              tidetext = tidetext + " The low tides are at "
           else:
              tidetext = " The low tide is at "
           for x in range(0,len(self.lowtidetimes[day])):
              tidetext = tidetext + self.lowtidetimes[day][x]
              if x != len(self.lowtidetimes[day])-1:
                 tidetext = tidetext + " and "
              else:
                 tidetext = tidetext + " .        "
           if len(self.lowtidetimes)>1:
              tidetext = tidetext + " The values are  "
           else:
              tidetext = tidetext + " The value is  "
           
           for x in range(0,len(self.lowtidetimes[day])):
              tidevalue = round(float(self.lowtidevalues[day][x]),1)
              tidetext = tidetext + str(tidevalue)
              if x != len(self.lowtidetimes[day])-1:
                 tidetext = tidetext + " and "
              else:
                 tidetext = tidetext + " feet.               "

                 #else:
        return reportText + tidetext 
        
    def printBestDayToSurf(self):
   
        indexdate = datetime.date.today()
        daydelta = datetime.timedelta(days = 1*self.bestdaytosurf)  
        bestsurfday = indexdate + daydelta
        if (self.bestdaytosurf ==0):
           reportText = "The best day to surf is today"
        else:
           reportText = "The Best Day to Surf is this upcoming " + bestsurfday.strftime("%A") + "."
 
        return reportText