import time
import RPi.GPIO as GPIO  # Import GPIO Library
import smtplib

DEL_PIN = 18
BTN_PIN = 17
BTN_ALARM_PIN = 12
ALARM_PIN = 22
SENSOR_PIN = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ALARM_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DEL_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_ALARM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, bouncetime=500)
GPIO.add_event_detect(BTN_ALARM_PIN, GPIO.FALLING, bouncetime=500)

def emailMe():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("popocoagulecole@gmail.com", "Popo21popo21ecole")

        subject = 'Alarm was triggerd'
        body = f'Your home alarm was triggered on'

        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail("popocoagulecole@gmail.com", "popocoagul@gmail.com", msg)


def getEvent():
    evenement = ""
    if GPIO.event_detected(BTN_PIN):
        evenement = "push"
    if GPIO.input(SENSOR_PIN) == True:
        evenement = "alarm"
    return evenement


def protocolAlarm():
    global etat
    print("send email")
    emailMe()
    print("alarm ON")
    while not GPIO.event_detected(BTN_PIN):
        GPIO.output(ALARM_PIN, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(ALARM_PIN, GPIO.LOW)
        time.sleep(0.25)
    etat = "reset"
    print("protocolAlarm return " + etat)
    return etat


def sysDelay():
    global etat
    etat = "armed"
    GPIO.remove_event_detect(BTN_ALARM_PIN)
    for x in range(10):
        GPIO.output(DEL_PIN, GPIO.HIGH)
        time.sleep(0.25)
        if GPIO.event_detected(BTN_PIN):
            print("sysDelaybr")
            etat = "reset"
            print("sysDelaybreak")
            break
        time.sleep(0.25)
        if GPIO.event_detected(BTN_PIN):
            print("sysDelaybr1")
            etat = "reset"
            print("sysDelaybreak1")
            break
        GPIO.output(DEL_PIN, GPIO.LOW)
        time.sleep(0.25)
        if GPIO.event_detected(BTN_PIN):
            print("sysDelaybr2")
            etat = "reset"
            print("sysDelaybreak2")
            break
            time.sleep(0.25)
        if GPIO.event_detected(BTN_PIN):
            print("sysDelaybr3")
            etat = "reset"
            print("sysDelaybreak3")
            break
        x += 1
    print("sysDelay return " + etat)
    return etat


def standByDelay():
    global etat
    etat = "alarmTrig"
    for x in range(12):
        GPIO.output(DEL_PIN, GPIO.HIGH)
        time.sleep(0.208)
        if GPIO.input(BTN_ALARM_PIN) == False:
            print("standByDelaybr")
            etat = "reset"
            print("standByDelaybreak")
            break
        time.sleep(0.208)
        if GPIO.input(BTN_ALARM_PIN) == False:
            print("standByDelaybr1")
            etat = "reset"
            print("standByDelaybreak1")
            break
        GPIO.output(DEL_PIN, GPIO.LOW)
        time.sleep(0.208)
        if GPIO.input(BTN_ALARM_PIN) == False:
            print("standByDelaybr2")
            etat = "reset"
            print("standByDelaybreak2")
            break
            time.sleep(0.208)
        if GPIO.input(BTN_ALARM_PIN) == False:
            print("standByDelaybr3")
            etat = "reset"
            print("standByDelaybreak3")
            break
        x += 1
    print("standByDelay return " + etat)
    return etat


etat = "unarmed"

while True:
    event = getEvent()

    if event == "push":
        time.sleep(0.2)
        if etat == "armed":
            print("reset")
            etat = "reset"
        if etat == "unarmed":
            print("arming")
            etat = "arming"

    if event == "alarm":
        if etat == "armed":
            print("triggered")
            standByDelay()


    if etat == "arming":
        sysDelay()
        print(etat)
        if etat == "arming":
            etat = "armed"
        print(etat + " from arming")

    if etat == "alarmTrig":
        protocolAlarm()

    if etat == "reset":
        GPIO.output(ALARM_PIN, GPIO.LOW)
        for x in range(4):
            GPIO.output(DEL_PIN, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(DEL_PIN, GPIO.HIGH)
            time.sleep(0.1)
            x += 1
        print("unarmed")
        etat = "unarmed"