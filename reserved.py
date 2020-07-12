import os, sys, string
import re, time
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__) 
PAGE_ACCESS_TOKEN = "EAADZCQZCd8FSABAFDZCw0mZCLVQZBqf9TRfU2XXKKEzUIJJ78Gla7a2qmi2WZChJzfCLzNZBJZAyRZBZCfWJEqNQYZBtUg8scZBCxcFbTtwJPFmHJMMVc2WFqssdDuZC756m50ZBZBhrnzskbLErG4PZCMk3XLOt4JrZCYORmr3pzjeRtyH9DGeGP5WZChDx5t"
bot = Bot(PAGE_ACCESS_TOKEN)
flag = 0

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    branch = db.Column(db.String(5))
    year = db.Column(db.String(7))
    contact = db.Column(db.String(10))
    sender_id = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

@app.route('/', methods=['GET'])
def verify(): 
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200 

@app.route('/', methods=['POST'])
def webhook():
    msg=["CSE","IT","EXTC"]
    yr=["FE", "SE", "TE", "BE", "BTECH", "DIPLOMA"]
    global flag
    print(flag)
    response=None
    data=request.get_json()
    log(data)
    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                #ids
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text='no text'

                    if flag == 6:
                        if "₹" not in messaging_text:
                            response = "you have already registered. Thank you."

                    if flag == 5:
                        if "contact" not in messaging_text and "valid" not in messaging_text:
                            if(re.match(r'[789]\d{9}$', messaging_text) != None):
                                print(messaging_text)
                                #code to sqlite
                                response = "please complete your registration by paying ₹ 50/- via UPI. \nFurther information is mailed to you. \nShare your payment screenshot on the given whatsapp number to confirm your seat. \nThis amount will be refunded on the workshop day itself. \nThanks for registering. :)"
                                flag=6
                            else:
                                response = "please enter a valid contact number."

                    if flag == 4:
                        if "year" not in messaging_text and "valid" not in messaging_text:
                            messaging_text = messaging_text.upper()
                            if messaging_text in yr:
                                print(messaging_text)
                                response = "please enter your contact number"
                                flag=5
                            else:
                                response = "please enter a valid year code as mentioned in message."

                    if flag == 3:
                        if "branch" not in messaging_text  and "valid" not in messaging_text:
                            messaging_text = messaging_text.upper()
                            if messaging_text in msg:
                                print(messaging_text)
                                response = "please enter your year.(For example, FE, SE, TE, BE, BTECH, DIPLOMA"
                                flag=4
                            else:
                                response = "please enter a valid branch code as mentioned in message."

                    
                    if flag == 2:
                        if "E-mail" not in messaging_text and "valid" not in messaging_text:
                            if(re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", messaging_text) != None):
                                print(messaging_text,sender_id)
                                #code to sqlite
                                response = "please enter your branch.(for example, CSE/IT/EXTC)"
                                flag=3
                            else:
                                response = "please enter a valid email address"

                    if flag==1:
                        if "name" not in messaging_text and "valid" not in messaging_text and "register" not in messaging_text:
                            if all(c in string.ascii_letters + ' ' for c in messaging_text):
                                print(messaging_text)
                                #code to sqlite
                                response = "please enter your E-mail address."
                                flag = 2
                            else:
                                response = "Please enter a valid name."

                    if flag==0:
                        entity,value = wit_response(messaging_text)
                        hello,dump = wit_response(messaging_text)


                        if hello == "hello":
                            response = "Hey, how may i help you!"
                        # if entity == "newstype":
                        #     response = "Ok, I will send you {} news".format(str(value))
                        # elif entity == "location":
                        #     response = "Ok, So you live in {0}. I will send you top headlines from {0}".format(str(value))
                        elif entity == "register" and messaging_text!="Try asking, I want to register.":
                            response = "please type your full name."
                            flag =1
                            print(flag)
                            print("hello")
                        if response == None:
                            response = "Try asking, I want to register."
                    bot.send_text_message(sender_id,response)
    return "ok", 200
    # if flag==3:
    #     bot.send_text_message(sender_id,"Please enter a valid contact.")
    #     flag =4
    #     return "ok", 200

    # if flag==4:
    #     bot.send_text_message(sender_id,"thanks.")
    #     return "ok",200




    
    
    
        
# def form():
#     msg,sid=webhook()
#     if not all(x.isalpha or x == "" for x in msg):
#         bot.send_text_message(sid,"Please enter a valid name or try asking (I want to register).")
#     else:
#         #code to sqlite
#         bot.send_text_message(sid,"please enter your E-mail address.")
                    
#     #email address
#     if(re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", msg) != None):
#         #code to sqlite
#         bot.send_text_message(sid,"please enter your branch.(for example, for CSE/IT/EXTC)")
#     else:
#         bot.send_text_message(sid,"Please enter a valid email address.")


#     if not all(x.isalpha or x == "" for x in msg):
#         bot.send_text_message(sid,"Please enter a valid branch name.")
#     else:
#         #code to sqlite
#         bot.send_text_message(sid,"please enter your E-mail address.")
#     return "ok",200

def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80) 
