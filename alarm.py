import RPi.GPIO as GPIO
import time
from discord_webhook import DiscordWebhook
from pathlib import Path
import os

webhook_url = "https://discord.com/api/webhooks/123456/abcdefg"

base_folder = Path(__file__).parent.resolve()

pir1 = 11
pir2 = 13
pir3 = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pir1, GPIO.IN)
GPIO.setup(pir2, GPIO.IN)
GPIO.setup(pir3, GPIO.IN)

p1_detected = False
p2_detected = False
p3_detected = False

#start a counter so a sensor doesn't spam the chat with detections
counter = 0

while True:
    pir1_state = GPIO.input(pir1)
    pir2_state = GPIO.input(pir2)
    pir3_state = GPIO.input(pir3)

    counter +=1
    
    #pir1
    time.sleep(1)
    if pir1_state==1:
        if p1_detected == False:
            p1_detected = True
            #camera capture stuff
            os.system("fswebcam -r 1280x720 --no-banner detected.png")
            
            try:
                webhook1 = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content="Sensor 1 detected movement")
                with open(f"{base_folder}/detected.png", "rb") as f:
                    webhook1.add_file(file=f.read(), filename='detected.png')
                webhook1.execute()
            except:
                print("Could not send the Webhook/Reach the internet")
            time.sleep(1)

    #pir2
    time.sleep(1)
    if pir2_state==1:
        if p2_detected == False:
            p2_detected = True
            try:
                webhook2 = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content="Sensor 2 detected movement")
                webhook2.execute()
            except:
                print("Could not send the Webhook/Reach the internet")
            time.sleep(1)


    #pir3
    time.sleep(1)
    if pir3_state==1:
        if p3_detected == False:
            p3_detected = True
            try:
                webhook3 = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content="Sensor 3 detected movement")
                webhook3.execute()
            except:
                print("Could not send the Webhook/Reach the internet")
            time.sleep(1)
    
    #reset the timer every 10 loops
    #if a sensor sent an alert, it will be silent for the next 10 loops
    if counter == 10:
        counter = 0
        p1_detected = False
        p2_detected = False
        p3_detected = False