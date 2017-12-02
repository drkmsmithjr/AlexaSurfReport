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
from surfreport import SurfSpot,spots,getsurfspots
import datetime



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

    
def create_numberOfTries_attributes(numberOfTries,surfspotname):
    return {"numOfTries": numberOfTries, "surfspotname":surfspotname }
  


def Get_Surf_Report_For_Spot(intent, session,spots):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    teststr = ""
    card_title = 'Surf Checker Surf Report'
    session_attributes = {}
    should_end_session = False
    # check day (int) should we get forecast for
    Day = 0
    surfspotname = ""
    number_tries = 0
    # check if the numberOfIntents attribute has been set.  If so, get the value and update.  If not, then set it.
    if session.get('attributes', {}) and "numOfTries" in session.get('attributes', {}):
        number_tries = session['attributes']['numOfTries']
    if session.get('attributes',{}) and "surfspotname" in session.get('attributes',{}):
        surfspotname = session['attributes']['surfspotname']
    

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
       spot = intent['slots']['SurfSpot']['value'].lower()
    else:
       spot = surfspotname
    if spot in spots:
        surfspotname = spot
        report = SurfSpot(spot, spots[spot][0], spots[spot][1], spots[spot][2], spots[spot][3])
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
    session_attributes = create_numberOfTries_attributes(number_tries,surfspotname)
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

            
def Get_Tide_Report_For_Spot(intent, session,spots):
    """ reports the tide report 
    """
    teststr = ""
    card_title = 'Surf Checker Tide Report'
    session_attributes = {}
    should_end_session = False
    # check day (int) should we get forecast for
    Day = 0
    number_tries = 0
    surfspotname = ""
    # check if the numberOfIntents attribute has been set.  If so, get the value and update.  If not, then set it.
    if session.get('attributes', {}) and "numOfTries" in session.get('attributes', {}):
        number_tries = session['attributes']['numOfTries']
    if session.get('attributes',{}) and "surfspotname" in session.get('attributes',{}):
        surfspotname = session['attributes']['surfspotname']
    
        
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
       spot = surfspotname
    if spot in spots:
        surfspotname = spot
        report = SurfSpot(spot, spots[spot][0], spots[spot][1], spots[spot][2], spots[spot][3])
        try:
           report.getTideReport()
           # test if the report should be for today or tomorrow
           if number_tries == 0:
              number_tries = 1
              speech_output = report.printTideReport(Day) + ".\n" +" "+teststr + " " +\
                           "Would you like another report?  "
              #session_attributes = create_numberOfTries_attributes(number_tries)
           else:
              number_tries = number_tries + 1
              #session_attributes = create_numberOfTries_attributes(number_tries)
              speech_output =  report.printTideReport(Day) + ".\n" +" "+teststr + " " +\
                           "Would you like another report?"
           reprompt_text = "Would you like another report?  "
           should_end_session = False
        except:
           speech_output = "The NOAA Tide server is being updated: please try back in a few days.  Would you like another report?"
           reprompt_text = "Would you like another report?  "
           should_end_session = False
    elif spot == "no":
        speech_output = "Have a nice Day."
        reprompt_text = " "
        should_end_session = True
    else:
        
        speech_output = "I'm not sure what your surf spot is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your surf spot is. " \
                        "For example: What is the Tide Report for Salt Creek"
#    if number_tries == 0:
    session_attributes = create_numberOfTries_attributes(number_tries,surfspotname)
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

            
def Best_Day_To_Surf_Spot(intent, session,spots):
    """ reports the tide report 
    """
    teststr = ""
    card_title = 'Surf Checker Best Day Report'
    session_attributes = {}
    should_end_session = False
    # check day (int) should we get forecast for
    Day = 0
    number_tries = 0
    surfspotname = ""
    # check if the numberOfIntents attribute has been set.  If so, get the value and update.  If not, then set it.
    if session.get('attributes', {}) and "numOfTries" in session.get('attributes', {}):
        number_tries = session['attributes']['numOfTries']
    if session.get('attributes',{}) and "surfspotname" in session.get('attributes',{}):
        surfspotname = session['attributes']['surfspotname']
    
        
    # string to modify the reply 
    daystring = " "
    today = datetime.datetime.now()

    if 'value' in intent['slots']['SurfSpot'] :
       spot = intent['slots']['SurfSpot']['value']
    else:
       spot = surfspotname
    if spot in spots:
        surfspotname = spot
        report = SurfSpot(spot, spots[spot][0], spots[spot][1], spots[spot][2], spots[spot][3])
        report.getReport()
        # test if the report should be for today or tomorrow
        if number_tries == 0:
           number_tries = 1
           speech_output = report.printBestDayToSurf() + ".\n" +" "+teststr + " " +\
                        "on this day" +\
                        report.printReport(report.bestdaytosurf) + ".\n" +\
                        "Would you like another report?  "
           #session_attributes = create_numberOfTries_attributes(number_tries)
        else:
           number_tries = number_tries + 1
           #session_attributes = create_numberOfTries_attributes(number_tries)
           speech_output = report.printBestDayToSurf() + ".\n" +" "+teststr + " " +\
                        "on this day" +\
                        report.printReport(report.bestdaytosurf) + ".\n" +\
                        "Would you like another report? "
        reprompt_text = "Would you like another report?  Just say the spot name"
        should_end_session = False
    elif spot == "no":
        speech_output = "Have a nice Day."
        reprompt_text = " "
        should_end_session = True
    else:
        speech_output = "I'm not sure what your surf spot is. " \
                        "Please try again and include the surf spot.  For example say: When is the best day to surf salt creek."
        reprompt_text = "I'm not sure what your surf spot is. " \
                        "For example say: When is the best day to surf Salt Creek"
#    if number_tries == 0:
    session_attributes = create_numberOfTries_attributes(number_tries,surfspotname)
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
            
def Get_Water_Temp_For_Spot(intent, session,spots):
    """ reports the tide report 
    """
    teststr = ""
    card_title = 'Surf Checker Water Temp Report'
    session_attributes = {}
    should_end_session = False
    # check day (int) should we get forecast for
    Day = 0
    number_tries = 0
    surfspotname = ""
    # check if the numberOfIntents attribute has been set.  If so, get the value and update.  If not, then set it.
    if session.get('attributes', {}) and "numOfTries" in session.get('attributes', {}):
        number_tries = session['attributes']['numOfTries']
    if session.get('attributes',{}) and "surfspotname" in session.get('attributes',{}):
        surfspotname = session['attributes']['surfspotname']
            
    # string to modify the reply 
    daystring = " "
    today = datetime.datetime.now()

    if 'value' in intent['slots']['SurfSpot'] :
       spot = intent['slots']['SurfSpot']['value']
    else:
       spot = surfspotname
    if spot in spots:
        surfspotname = spot
        report = SurfSpot(spot, spots[spot][0], spots[spot][1], spots[spot][2], spots[spot][3])
        #teststr = str(spots[spot][3]) + " " + str(spot) + " "
        report.getWaterTemp()
        #teststr = teststr + "water temp =" + str(report.waterTemp) + " " + str(report.noaaWaterTempUrl)
        # test if the report should be for today or tomorrow
        if number_tries == 0:
           number_tries = 1
           speech_output = report.printWaterTemp() + ".\n" +" "+teststr + " " +\
                        "Would you like another report?  "
           #session_attributes = create_numberOfTries_attributes(number_tries)
        else:
           number_tries = number_tries + 1
           #session_attributes = create_numberOfTries_attributes(number_tries)
           speech_output = report.printWaterTemp() + ".\n" +" "+teststr + " " +\
                        "Would you like another report? "
        reprompt_text = "Would you like another report?  Just say the spot name"
        should_end_session = False
    elif spot == "no":
        speech_output = "Have a nice Day."
        reprompt_text = " "
        should_end_session = True
    else:
 
        speech_output = "I'm not sure what surf spot to use with the water temperature report. " \
                        "Please try again including the surf spot in the report request."
        reprompt_text = "I don't recognize the surf spot you would like.    Please try another report request and ask for help to more info. " \
                        "For example say: What is the water temp at Salt Creek"
#    if number_tries == 0:
    session_attributes = create_numberOfTries_attributes(number_tries,surfspotname)
    return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))

            
            
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome from Surf Checker"
    speech_output = "Welcome to the Surf Checker.   " \
                    "Please tell me the surf spot you need the surf or Tide forecast for.   For example say, " \
                    "what is the surf report for salt creek?" \
                    "For a surf report, You can also just say the surf spot name.  For example, "\
                    "say Lowers, or Salt Creek,      "\
                    "Once you have received a surf report for a spot, Alexa will remember "\
                    " this spot and you can get other reports without having to repeat the surf spot. "\
                    " For example: You can just say ," \
                    " What is the tide report?" \
                    " Or you can say, when is the best day to surf?"\
                    " To continue just say the spot name, ask for a report or ask for more help."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the spot you are looking for by saying a surf spot, " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Getting Help for Surf Checker"
    speech_output = "To get the surf forecast, Tide forecast, or water temperature reports you need to include the spot name,   "\
                    "For example say, " \
                    "what is the surf report for salt creek?" \
                    "or say, What is the tide report for Huntington State Beach on Tuesday?" \
                    "or say, what is the water temperature at county line"\
                    "For a surf report, You can also just say the surf spot name.  For example, just say uppers, lowers, Salt Creek," \
                    "or Huntington state beach. " \
                    "Once you have received a surf report for a spot, Alexa will remember "\
                    " this spot and you can get other reports without having to repeat the surf spot. "\
                    " For example: You can just say ," \
                    " What is the tide report?" \
                    " Or you can say, when is the best day to surf?" \
                    " Or you can say, what is the water temperature?" \
                    " I hope this helps.  To continue just say the spot "\
                    " name, ask for a report or ask for more help."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the spot you are looking for by saying a surf spot, " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
               

def handle_session_end_request():
    card_title = "Thank you for trying the Surf Checker"
    speech_output = "Thank you for trying the surf checker ." \
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
    allspots = {}
    allspots = getsurfspots(spots)    
    
    # Dispatch to your skill's intent handlers
    if intent_name == "GetSurfReportForSpot":
        return Get_Surf_Report_For_Spot(intent, session,allspots)
    elif intent_name == "GetTideReportForSpot":
        return Get_Tide_Report_For_Spot(intent, session,allspots)
    elif intent_name == "BestDayToSurfSpot":
        return Best_Day_To_Surf_Spot(intent, session,allspots)
    elif intent_name == "GetWaterTempForSpot":
        return Get_Water_Temp_For_Spot(intent, session,allspots)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
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