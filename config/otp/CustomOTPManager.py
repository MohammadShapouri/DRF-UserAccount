from .utils import OTPManager
from rest_framework.response import Response
from rest_framework import status



class CustomAccountVerificationOTPManager(OTPManager):
    def afterValidationAction(self, user):
       user.is_active = True
       user.is_account_verified = True
       user.save()
       return self.successfulValidationMsg()
    
    def successfulValidationMsg(self):
        return Response(data={'OTP': "Account verified."}, status=status.HTTP_200_OK)



class CustomNewPhoneNumberVerificationOTPManager(OTPManager):
    def afterValidationAction(self, user):
       user.is_new_phone_verified = True
       user.save()
       return self.successfulValidationMsg()
    
    def successfulValidationMsg(self):
        return Response(data={'OTP': "New phone number verified."}, status=status.HTTP_200_OK)



class CustomForgetPasswordOTPManager(OTPManager):
    def afterValidationAction(self, user):
       return True



class CustomOTPLogin(OTPManager):
    def afterValidationAction(self, user):
       return True