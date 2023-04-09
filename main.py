"""
To use this code you must set up some sort of server and link it to your twilio account to handle incoming texts, like ngrok
Replace all environ variables with your own tokens/id's
"""

import os
from twilio.rest import Client
from flask import *
import openai
import time

openai.api_key = os.environ["OPEN_AI_KEY"]

app = Flask("FoodBotSMS")

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def send_sms(text):
    message = client.messages.create(
        body=text,
        from_=os.environ["TWILIO_NUM"],
        to=os.environ["PHONE_NUM"]
    )
def send_image(text, image_url):
    message = client.messages.create(
        body=text,
        from_=os.environ["TWILIO_NUM"],
        to=os.environ["PHONE_NUM"],
        media_url=[image_url],
    )

@app.route("/sms", methods=["POST", "Get"])
def sms():

    message = request.values.get("Body", '').lower()

    if message[:7] == "recipe:":
        send_sms('Keep in mind the requirements have to make sense or else the resulting recipe will not make sense')

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Give me a recipe with the following requirements: {message[7:]} "}]
        )
        print(completion["choices"][0]["message"]["content"])
        send_sms(completion["choices"][0]["message"]["content"])
    elif message[:9] == "pomodoro:":
        if message[9:].isdigit():
            send_sms('Starting pomodoro working technique.')
            for i in range(int(message[9:])):
                send_image('25 working minute period started!', "https://cdn.pixabay.com/photo/2021/11/11/23/18/tomato-6787483_960_720.png")
                time.sleep(1500)
                send_image('5 minute break period started!', "https://live.staticflickr.com/65535/50428246811_8a7c95c262_b.jpg")
                time.sleep(300)
            send_image("Good Job! Your work/study period is over!", "https://cdn.pixabay.com/photo/2022/12/11/04/11/thumbs-up-7648171_960_720.png")
        else:
            print(message[10:])
            send_sms('Please enter an integer!')
    else:
        send_sms('Please either type "pomodoro:" or "recipe:" as commands!')
app.run()
