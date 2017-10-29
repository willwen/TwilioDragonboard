##Run Twlio Server on Dragonboard 410c and blink led when messages are received
##Submission for Boston Hacks 2017
##Ashley Cui
##Sherry Mei
##Will Wen
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
import random
import time
#https://github.com/96boards/96BoardsGPIO
from gpio_96boards import GPIO

app = Flask(__name__)

GPIO_A = GPIO.gpio_id('GPIO_A')
pins = (
    (GPIO_A, 'out'),
)



@app.route("/sms", methods=['GET', 'POST'])
def sms():
    blink(GPIO(pins))
    resp = MessagingResponse()

    # msg.media("https://i.ytimg.com/vi/sAqks9CB6mg/maxresdefault.jpg")

    body = request.values.get('Body', None)
    # Add a message
    # resp.message()
    listfrm=body.split(' ')
    greetings_list = ['hi','hello','hey']
    
    if listfrm.length >= 2:
    	if listfrm[0].lower()=='remind' and listfrm[1].lower() =='me':
	        print("reminded")
	        resp.message("REMINDERTIME!!")
	elif body.lower() in greetings_list:
            random_greetings=random.choice(greetings_list)
            resp.message(random_greetings)
    elif body == 'bye':
    	resp.message("Bye! :)")
    return str(resp)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    blink(GPIO(pins))
    callers = { "+18577010279": "Sherry"}
    from_number = request.values.get('From', None)
    print ("calling")
    if from_number in callers:
        caller = callers[from_number]
    else:
        caller = "Monkey"
    resp = VoiceResponse()
    resp.say("Hello " + caller)
    gather = Gather(num_digits=1, action='/storytime')
    gather.say('To listen to Three Little Pigs, press 1. To listen to Little Red Riding Hood, press 2.')
    resp.append(gather)
    return str(resp)


@app.route("/storytime", methods=['GET', 'POST'])
def storytime():
    blink(GPIO(pins))
    if 'Digits' in request.values:
        choice = request.values['Digits']
        if choice == '1':
            f = open('threelittlepigs.txt', 'r')
            lines = f.readlines()
            for line in lines:
                resp.say(line)
		resp.redirect("/voice")
	    	return str(resp)
        elif choice == '2':
            g = open('littlered.txt', 'r')
	    lines = g.readlines()
	    for line in lines:
                resp.say(line)
                resp.redirect("/voice")
	    return str(resp)
        else:
            resp.say("Sorry, I don't understand that choice.")
	    resp.redirect("/voice")
            return str(resp)

def blink(gpio):
    for i in range(3):
        gpio.digital_write(GPIO_A, GPIO.HIGH)
        time.sleep(500)
        gpio.digital_write(GPIO_A, GPIO.LOW)
        time.sleep(500)

if __name__ == "__main__":
	app.run(debug=True)
