from celery import shared_task



@shared_task
def send_SMS(OTP_code):
    print('OTP Code is: ', OTP_code)