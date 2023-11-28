from time import sleep
from celery import shared_task



@shared_task
def sendSMS(OTPCode):
    sleep(10)
    print('OTP Code is: ', OTPCode)