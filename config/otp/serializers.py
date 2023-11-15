from rest_framework import serializers
from .models import OTPCode
from otpConfig.otpConfig import OTPConfig



class OTPVerifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTPCode
        fields = ['user_pk', 'otp']


    def validate_OTP(self, value):
        OTP = str(value)
        if len(OTP) is not OTPConfig.OTPLength:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain " + OTPConfig.OTPLength + " characters."})
        elif str.isdigit(OTP) is False:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must not contain characters."})
        return True


    # def validate_otp_type(self, value):
    #     validOTPTypeInputs = ['timer_counter_based', 'counter_based', 'timer_based']
    #     if value not in validOTPTypeInputs:
    #         raise serializers.ValidationError({'otp_type': "otp_type must be one of %r." % validOTPTypeInputs})



    # def validate_otp_usage(self, value):
    #     validOTPUsageInputs = ['account_verification', 'new_phone_number_verification', 'forget_password', 'OTP_login']
    #     if value not in validOTPUsageInputs:
    #         raise serializers.ValidationError({'otp_usage': "otp_usage must be one of %r." % validOTPUsageInputs})

