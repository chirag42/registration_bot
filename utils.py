from wit import Wit
access_token ="53T2ZGIG6XC322SJDVN65GSBLKLZNB3Q"
client = Wit(access_token = access_token)

def wit_response(message_text):
    resp = client.message(message_text)
    print("chirag")
    print(resp)
    print("chirag")
    if resp['_text'] == "Hello" or resp['_text'] == "hello":
        return "hello","cric" 
    entity = None
    value= None
    try:
        entity=list(resp['entities'])[1]
        value =resp['entities'][entity][0]['value']
    except:
        pass
    return(entity,value)
#print(wit_response("i want sports news"))
