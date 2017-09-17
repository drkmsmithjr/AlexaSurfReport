"""
mySurfReport

#Written by Mark Smith, www.surfncircuits.com
#Based on the Amazon Alexa Skills Color Kit
#Based on Code Written by Colin Karpfinger
# http://punchthrough.com/bean
# http://punchthrough.com/bean/examples/surf-report-notifier/
# https://github.com/PunchThrough/BeanSurfMap
# copyright (c) 2014 Punch Through Design
"""


from __future__ import print_function

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

    
def create_numberOfTries_attributes(numberOfTries):
    return {"numOfTries": numberOfTries }
    
    
# defining the surf spots

spots = {
    'uppers':["4738","2950"],
    'upper trestles':["4738","2950"],
    'upper':["4738","2950"],
    'salt creek':["4233","2950"],
    'doheny':["4848","2950"],
    'doheny state beach':["4848","2950"],
    'lowers':["4740","2950"],
    'lower trestles':["4740","2950"],
    'lower':["4740","2950"],
    't-street':["4235","2950"],
    'T. street' :["4235","2950"],
    'san clementi state beach':["4843","2950"],
    'the point':["4237","2950"],
    'old mans':["109918","2950"],
    'hb pier':["4874","2143"],
    'HB pier':["4874","2143"],
    'h. b. pier':["4874","2143"],
    'Huntington beach pier':["4874","2143"],
    '56th street':["43103","2143"],
    'fifty sixth street':["43103","2143"],
    'the wedge':["4232","2143"],
    'goldenwest':["4870","2143"],
    'golden west':["4870","2143"],
    'huntington state beach':["103681","2143"],
    'Huntington state beach':["103681","2143"],
    'seal beach':["4217","2143"],
    'bolsa chica':["4868","2143"],
    'bolsa chica state beach':["4868","2143"],
    'Newport point':["4877","2143"],
    'blackies':["53412","2143"]    
}



# --------------- Functions that control the skill's behavior ------------------


# Class Surfspot uses the 
# Surfline API Report Parser 
# modified by Mark Smith
# www.surfncircuit.com
# removed the tide information
# Used surfMax and surfMin from spot report and regional report 
# added SurfText inputs.    

# Based on Code Written by Colin Karpfinger
# http://punchthrough.com/bean
# http://punchthrough.com/bean/examples/surf-report-notifier/
# https://github.com/PunchThrough/BeanSurfMap
# copyright (c) 2014 Punch Through Design

import datetime
import urllib2
import json
import time
from decimal import *
import string

daysInReport = 6
conditionTypes=["","flat", "very poor", "poor","poor to fair","fair","fair to good","good","very good","good to epic","epic"]

#lowTides=[]
#highTides=[]

class SurfSpot:
    baseUrl="http://api.surfline.com/v1/forecasts/0000?resources=surf,analysis&days=6&getAllSpots=false&units=e&interpolate=false&showOptimal=false"
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
    
    def __init__(self, spotName, spotID, regionalID):
        # create object with the spot name, spotID and regionalID.  Both are available in HTTP addresss associaed with  
        # the surfline.com site.    
        self.spotName = spotName
        self.surflineUrl=self.baseUrl.replace("0000",spotID)
        self.surflineRegionalUrl=self.baseUrl.replace("0000",regionalID)

        self.heightsMax=[]
        self.heightsMin=[]
        self.surfText=[]
        self.regionalConditions=[]
        
    def getReport(self):
        # use the spot API to get the current information
        # use the regional API address (regionalReport) to get the forecast information
        
        webreq = urllib2.Request(self.surflineUrl, None, {'user-agent':'syncstream/vimeo'})
        opener = urllib2.build_opener()
        f = opener.open(webreq)
        fstr = f.read()
        fstr = fstr.replace(')','') #remove closing )
        fstr = fstr.replace(';','') #remove semicolon
        fstr = fstr.strip() #remove any whitespace in start/end
        rep = json.loads(fstr)

        webreq = urllib2.Request(self.surflineRegionalUrl, None, {'user-agent':'syncstream/vimeo'})
        opener = urllib2.build_opener()
        f = opener.open(webreq)
        fstr = f.read()
        fstr = fstr.replace(')','') #remove closing )
        fstr = fstr.replace(';','') #remove semicolon
        fstr = fstr.strip() #rem3ove any whitespace in start/end
        regionalReport=json.loads(fstr)


        self.surflineName=rep["name"]
        for day in range(0,daysInReport):
            daysAvgMax=0
            daysAvgMin=0
            self.regionalConditions.append(conditionTypes.index(regionalReport["Analysis"]["generalCondition"][day]))
            if day == 0:
               if (len(rep["Analysis"]["surfMax"]) > 0) :
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


def Get_Surf_Report_For_Spot(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    teststr = ""
    card_title = 'Surf Checker Surf Report'
    session_attributes = {}
    should_end_session = False
    # check day (int) should we get forecast for
    Day = 0
    
    number_tries = 0
    # check if the numberOfIntents attribute has been set.  If so, get the value and update.  If not, then set it.
    if session.get('attributes', {}) and "numOfTries" in session.get('attributes', {}):
        number_tries = session['attributes']['numOfTries']
        #session_attributes = create_numberOfTries_attributes(number_tries)
        #teststr = " the number of tries was again 1 "
        #session.update('numberOfTries') = number_tries
    #else:
    #    number_tries = 0
        #session_attributes = create_numberOfTries_attributes(number_tries)
    
    
    # string to modify the reply 
    daystring = " "
    today = datetime.datetime.now()

    if 'SurfDay' in intent['slots']:
        if 'value' in intent['slots']['SurfDay']:
            a = intent['slots']['SurfDay']['value']
            surfdate = datetime.datetime.strptime(a,'%Y-%m-%d')
            DayTimeDelta = surfdate - today
            # subtract three hours from the time.   I assume the time is ireland time.
            Day = int((DayTimeDelta.total_seconds() + (60*60*6)) /(60*60*24) + 1)
            if Day > 6 or Day < 0 :
                #daystring = "We have the forecast for only 6 days.  "
                Day = 0
            else:
                if Day == 0:
                   daystring = "today for "
                elif Day == 1:
                   daystring = "tomorrow for"
                elif Day >= 2:
                   daystring = surfdate.strftime('%A') + " for "
        else:
            daystring = " "
        

    if 'value' in intent['slots']['SurfSpot'] :
       spot = intent['slots']['SurfSpot']['value']
    else:
       spot = 'NoSpotDecodedByAlexa'
    if spot in spots:
        report = SurfSpot(spot, spots[spot][0], spots[spot][1])
        report.getReport()
        # test if the report should be for today or tomorrow
        if number_tries == 0:
           number_tries = 1
           speech_output = "The surf Report for " + \
                        daystring + \
                        report.printReport(Day) + ".\n" +" "+teststr + " " +\
                        "Would you like another report?  Just say the spot name."
           #session_attributes = create_numberOfTries_attributes(number_tries)
        else:
           number_tries = number_tries + 1
           #session_attributes = create_numberOfTries_attributes(number_tries)
           speech_output = "The surf Report for " + \
                        daystring + \
                        report.printReport(Day) + ".\n" +" "+teststr + " " +\
                        "Would you like another report?"
        reprompt_text = "Would you like another report?  Just say the spot name"
        should_end_session = False
    elif spot == "no":
        speech_output = "Have a nice Day."
        reprompt_text = " "
        should_end_session = True
    else:
        speech_output = "I'm not sure what your surf spot is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your surf spot is. " \
                        "You can try again buy saying just the spot name, " \
                        "Some examples are lowers, or salt creek."
#    if number_tries == 0:
    session_attributes = create_numberOfTries_attributes(number_tries)
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
#    else:
#     return build_response(session_attributes, build_speechlet_response(
#            card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome from Surf Checker"
    speech_output = "Welcome to the Surf Checker.   " \
                    "Please tell me the surf spot you need the forecast for.   For example say, " \
                    "what is the surf report for salt creek?" \
                    "You can also just say the surf spot name.  For example, just say uppers, lowers, Salt Creek," \
                    "or Huntington state beach.  , "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the spot you are looking for by saying a surf spot, " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Thank you for trying the Surf Checker"
    speech_output = "Thank you for trying the surf checker." \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

        
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    
    # Dispatch to your skill's intent handlers
    if intent_name == "GetSurfReportForSpot":
        return Get_Surf_Report_For_Spot(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])