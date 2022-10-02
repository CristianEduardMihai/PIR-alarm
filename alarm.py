import RPi.GPIO as GPIO
import time
import cv2
from discord_webhook import DiscordWebhook
from pathlib import Path

webhook_url = "https://discord.com/api/webhooks/1026212740760600587/_i6K6cnXgI78bc92W4vINgk8L-VBFYiRY9d6WJkMzx4qfSyjrR5nqMNjzZhNPIcsuWCT"

base_folder = Path(__file__).parent.resolve()

pir1 = 11
pir2 = 13
pir3 = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pir1, GPIO.IN)
GPIO.setup(pir2, GPIO.IN)
GPIO.setup(pir3, GPIO.IN)

#in this example, the camera is attached to pir1

# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that
# By copying the code bellow you can add multiple cameras to multiple sensors.
# cam1, cam2 and so on.
cam_port = 0
cam = cv2.VideoCapture(cam_port)

while True:
    pir1_state = GPIO.input(pir1)
    pir2_state = GPIO.input(pir2)
    pir3_state = GPIO.input(pir3)
    
    #pir1
    time.sleep(1)
    if pir1_state==1:
        print("S1 detected")

        #camera capture stuff
        image = cam.read()
        cv2.imwrite("detected.png", image)

        webhook1 = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content="Sensor 1 detected movement")
        with open(f"{base_folder}/detected.png", "rb") as f:
            webhook1.add_file(file=f.read(), filename='detected.png')
        webhook1.execute()
        time.sleep(1)

    
    #pir2
    time.sleep(1)
    if pir2_state==1:
        webhook2 = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content="Sensor 2 detected movement")
        webhook2.execute()
        time.sleep(1)


    #pir3
    time.sleep(1)
    if pir3_state==1:
        webhook3 = DiscordWebhook(url=webhook_url, rate_limit_retry=True, content="Sensor 3 detected movement")
        webhook3.execute()
        time.sleep(1)
        