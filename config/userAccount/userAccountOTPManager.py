from otp.utils.baseOTPManager import BaseOTPManager
from rest_framework.response import Response
from rest_framework import status



class UserAccountOTPManager(BaseOTPManager):
    config = {
            'defaultOTPLength': 8, 
            'defaultMaxPossibleTry': 5,
            'defaultExpireAfter': 120,
            'configProfiles': {
            'account_verification':{
                'OTPType': 'timer_counter_based',
                'OTPUsage': 'Account Verification',
                'maxPossibleTry': 3
            },
            'new_phone_number_verification': {
                'OTPType': 'counter_based',
                'OTPUsage': 'New Phone Number Verification',
            },
            'reset_password': {
                'OTPType': 'timer_counter_based',
                'OTPUsage': 'Forgotten Password',
                'expireAfter': 600
            }
            }
        }


class UserAccountVerificationOTPManager(UserAccountOTPManager):
    def afterOTPVerificationAction(self, user):
        user.is_active = True
        user.is_account_verified = True
        user.save()
        return self.successfulValidationMsg()
    
    def successfulValidationMsg(self):
        return Response(data={'OTP': "Account verified."}, status=status.HTTP_200_OK)



class UserAccountNewPhoneNumberVerificationOTPManager(UserAccountOTPManager):
    def afterOTPVerificationAction(self, user):
       user.is_new_phone_verified = True
       user.phone_number = user.new_phone_number
       user.new_phone_number = None
       user.save()
       return self.successfulValidationMsg()

    def successfulValidationMsg(self):
        return Response(data={'OTP': "New phone number verified."}, status=status.HTTP_200_OK)



class ResetPasswordOTPManager(UserAccountOTPManager):
    def afterValidationAction(self, user):
       return True
