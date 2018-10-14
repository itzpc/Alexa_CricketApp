import json

# Builders
def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

#Responses
def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)
def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


#Custom Intent
def Fav_Num_Intent(event,content):
    favNum= "My Fav number is 7"
    return statement("fav_Num_intent_card", favNum)
def scoreNum_intent(event,content):
    slot=event['request']['intent']['slots']
    number="You Have Scored "+slot['score']['value']+"!"
    return statement("NumSlot",number)
def scorePhrase_intent(event,content):
    slot=event['request']['intent']['slots']
    Phrase="That was a "+slot['shotDescription']['value']+" shot !"
    return statement("NumSlot",Phrase)


def scoreNum_intent(event,content):
    slot=event['request']['intent']['slots']
    number="You Have Scored "+slot['score']['value']+"!"
    return statement("NumSlot",number)

def scorePhrase_intent(event,content):
    slot=event['request']['intent']['slots']
    Phrase="That was a "+slot['shotDescription']['value']+" shot !"
    return statement("NumSlot",Phrase)

def Session_Intent(event,content):
    """
    in order to maintain the session , return the session object in every response
    """
    if 'attributes' in event['session']:
        session_attributes=event['session']['attributes']
        if 'counter' in session_attributes:
            session_attributes['counter']+=1
        else:
            session_attributes['counter']=1
    else:
        event['session']['attributes']={}
        session_attributes=event['session']['attributes']
        if 'counter' not in session_attributes:
            session_attributes['counter']=1
    return conversation("SessionIntent",session_attributes['counter'],session_attributes)


#Routing
def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents

    if intent == "FavNumIntent":
        return Fav_Num_Intent(event, context)

    if intent== "scoreNum":
        return scoreNum_intent(event, context)
    if intent == "scorePhrase":
        return scorePhrase_intent(event,context)

    if intent == "SessionIntent":
        return Session_Intent(event,context)

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()

# On Launch
def on_launch(event, context):
    return statement("title", "Hello World")

# Main - Entry
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
