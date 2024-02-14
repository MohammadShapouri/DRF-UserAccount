from otp.utils.base_OTP_manager import BaseOTPManager
from rest_framework.response import Response
from rest_framework import status



class UserAccountOTPManager(BaseOTPManager):
    config = {
            'default_OTP_length': 8, 
            'default_max_possible_try': 5,
            'default_expire_after': 600,
            'config_profiles': {
            'account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
                'max_possible_try': 3
            },
            'new_phone_number_verification': {
                'OTP_type': 'counter_based',
                'OTP_usage': 'New Phone Number Verification',
            },
            'reset_password': {
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Forgotten Password'
            }
            }
        }



class UserAccountVerificationOTPManager(UserAccountOTPManager):
    def after_OTP_verification_action(self, user):
        user.is_active = True
        user.is_account_verified = True
        user.save()
        return self.successful_validation_message()
    
    def successful_validation_message(self):
        return Response(data={'OTP': "Account verified."}, status=status.HTTP_200_OK)



class UserAccountNewPhoneNumberVerificationOTPManager(UserAccountOTPManager):
    def after_OTP_verification_action(self, user):
       user.is_new_phone_verified = True
       user.phone_number = user.new_phone_number
       user.new_phone_number = None
       user.save()
       return self.successful_validation_message()

    def successful_validation_message(self):
        return Response(data={'OTP': "New phone number verified."}, status=status.HTTP_200_OK)



class ResetPasswordOTPManager(UserAccountOTPManager):
    def after_OTP_verification_action(self, user):
       pass
