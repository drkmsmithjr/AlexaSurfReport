# AlexaSurfReport
Alexa Surf Report Skill

Check out the full blog at www.surfncircuits.com
[**"Creating the "Surf Checker".  An Amazon Echo Skill"**](http://surfncircuits.com/2017/10/28/creating-the-surf-checker-an-amazon-echo-skill/)

This file shows the Lambda function portion of the Amazon Surf Checker skill.    This function will generate a surf report that will be used by Alexa to report.

New surf locations are shown in the surfspot.cvs file.  To add additional spots,    You need the following:
* "location name"
* the SpotID
* regional ID
* NOAA Tide locater ID.    
 
The location name, SpotID, and regional ID can be taken from the HTTP address of the corresponding surfline.com surf report and the NOAA tide database located at https://tidesandcurrents.noaa.gov.  After adding, please submit a pull request and I'll add to master.   

In order to define new surf spots for the surfspots.cvs file.    You need to add the Location name, surfspotID, reginal ID, and TideID to the file:

* Get the surf spot name:  You can use any name you want, but they may need to be adjusted to work best with Alexa.   Please supmit your name and we will review to compatibility.   

* Getting the SurfSpotID:   You do this by finidng the approprite surfline.com surf report and find the SpotID in the web  address.   
    * For example: The web report address for Salt Creek surfline.com surf report is: http://www.surfline.com/surf-report/salt-creek-southern-california_4233/.  From this web page, the SurfID = 4233.  You can see this number in the web site address above.

* Getting the RegionalID:    You can do this by finding the appropriate surfline.com reginal report page and finding the ID in the web address. 
  *  For example the regional ID for salt creek is on the south orange county regional report:
http://www.surfline.com/surf-forecasts/southern-california/south-orange-county_2950/.  On this page, the RegionalIP = 2950.

* Getting the NOAA Tide ID location: You do this by finding the closest TideID from the NOAA WEb page:
 https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1393.
    * For example: the closest Tide Sensor ID for salt Creek will be San Clemente. 
the NOAA_TideID = TWC0419 

    * verify you get tide data using the following format
 https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20171104&end_date=20171105&datum=MLLW&station=XXXXXX&time_zone=lst_ldt&units=english&interval=hilo&format=json where you replace XXXXXX with the NOAA_TideID name: (i.e. TWC0419)
  
* Add this data to a row of the surfspot.cvs file.  If you are adding a surf spot for a new region, please also add a row with the regional name.    
  
By Mark Smith, www.Surfncircuits.com
copyright (c) 2017 www.surfncircuits.com


The surfline API code was modified from 

Code Written by Colin Karpfinger
https://github.com/PunchThrough/BeanSurfMap

copyright (c) 2014 Punch Through Design

