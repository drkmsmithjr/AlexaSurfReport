# AlexaSurfReport
Alexa Surf Report Skill

Check out the full blog at www.surfncircuits.com
**"Creating the "Surf Checker".  An Amazon Echo Skill"**

This file shows the Lambda function portion of the Amazon Surf Checker skill.    This function will generate a surf report that will be used by Alexa to report.

By Mark Smith, www.Surfncircuits.com
copyright (c) 2017 www.surfncircuits.com

Code was modified from the Alexa Skills Kit and uses the www.surfline.com API

New surf locations are shown in the surfspot.cvs file.  To add additional spots,    You need the following:
* "location name"
* the SpotID
* regional ID
* NOAA Tide locater ID.    
 
The location name, SpotID, and regional ID can be taken from the HTTP address of the corresponding surfline.com surf report and the NOAA tide database located at https://tidesandcurrents.noaa.gov


The surfline API code was modified from 

Code Written by Colin Karpfinger
https://github.com/PunchThrough/BeanSurfMap

copyright (c) 2014 Punch Through Design

