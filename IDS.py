import RPi.GPIO as GPIO
from datetime import datetime
import time
import picamera
import Email
from firebase import firebase

GPIO.setmode(GPIO.BCM)

# Shooting Video and capturing image from the Pi camera
def picamerause(num):
    camera = picamera.PiCamera()
    camera.capture('image' + str(num) + '.jpg')
    time.sleep(1)
    camera.start_recording('video' + str(num) + '.h264')
    time.sleep(5)
    camera.stop_recording()
    time.sleep(1)
    camera.capture('image' + str(num) + '_2.jpg')
    camera.close()

def post_to_firebase(flag):
    

    res = ["Yes", "No"]
    fire = firebase.FirebaseApplication('https://fir-app-b50e6.firebaseio.com/')
    dt = datetime.now()
    date = dt.strftime('%d-%b-%Y')
    time = dt.strftime('%I:%M %p')
    result = fire.post(url='https://fir-app-b50e6.firebaseio.com/',data='{}\t\t\t\t{}\t\t\t\t\t\t\t\t\t\t{}'.format(date,time,res[flag]))

def main():
    # use Raspberry Pi board pin numbers
    # set GPIO Pins
    pinTrigger = 23
    pinEcho = 24
    

    # set GPIO input and output channels
    GPIO.setup(pinTrigger, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)
    GPIO.setup(18,GPIO.OUT)
    num = 0

    while True:
        GPIO.output(pinTrigger, False)
        time.sleep(1)
        # set Trigger to HIGH
        GPIO.output(pinTrigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(pinTrigger, False)

        startTime = time.time()
        stopTime = time.time()

        # save start time
        while 0 == GPIO.input(pinEcho):
            startTime = time.time()

        # save time of arrival
        while 1 == GPIO.input(pinEcho):
            stopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = stopTime - startTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        print("Distance: %.1f cm" % distance)
        if (distance <= 60):
            num += 1
            print('Capturing video and Photo of Intruder...')
            #TODO 
            picamerause(num)
            print("Sending Mail......")
            Email.sendMail(num)
            print("Waiting for User's command...")
            res = Email.read_email_from_gmail()
            if res:
##                GPIO.output(red, False)
##                GPIO.output(yellow, False)
##                GPIO.output(green, True)
                pwm=GPIO.PWM(18,50)
                pwm.start(7.5)
                time.sleep(10)
                pwm.ChangeDutyCycle(12.5)
                time.sleep(1)
                pwm.stop()
                #GPIO.cleanup()
            post_to_firebase(res)

    GPIO.setwarnings(False)
    GPIO.cleanup()

if __name__=='__main__':
    main()

