import RPi.GPIO as GPIO
from datetime import datetime
import picamera
import Email

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
    from firebase import firebase

    res = ["Yes", "No"]
    fire = firebase.FirebaseApplication('https://fir-app-b50e6.firebaseio.com/')
    dt = datetime.now()
    date = dt.strftime('%d-%b-%Y')
    time = dt.strftime('%I:%M %p')
    result = fire.post(url='https://fir-app-b50e6.firebaseio.com/',
                       data=f'{date}\t\t\t\t{time}\t\t\t\t\t\t\t\t\t\t{res[flag]}')

def main():
    # use Raspberry Pi board pin numbers
    # set GPIO Pins
    pinTrigger = 18
    pinEcho = 24
    yellow = 17
    green = 27
    red = 22

    # set GPIO input and output channels
    GPIO.setup(pinTrigger, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)
    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(yellow, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)

    num = 0

    while True:
        # set Trigger to HIGH
        GPIO.output(pinTrigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(pinTrigger, False)
        GPIO.output(red, True)
        GPIO.output(yellow, False)
        GPIO.output(green, False)

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
            GPIO.output(yellow, True)
            GPIO.output(red, False)
            GPIO.output(green, False)
            picamerause(num)
            print("Sending Mail......")
            mail.sendMail(num)
            print("Waiting for User's command...")
            res = read_email_from_gmail()
            if res:
                GPIO.output(red, False)
                GPIO.output(yellow, False)
                GPIO.output(green, True)
                time.sleep(10)
            post_to_firebase(res)

        time.sleep(1)
    GPIO.setwarnings(False)
    GPIO.cleanup()

if __name__=='__main__':
    main()
