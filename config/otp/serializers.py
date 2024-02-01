from rest_framework import serializers
from .utils.acceptable_OTP_values import least_acceptable_OTP_length, most_acceptable_OTP_length

class OTPVerifierSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['otp'] = serializers.CharField(required=True, label='OTP Code', allow_null=False)


    def validate_otp(self, value):
        if str.isdigit(value) is False:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must not contain characters."})
        if len(value) < least_acceptable_OTP_length:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain at least " + least_acceptable_OTP_length + " characters."})
        if len(value) > most_acceptable_OTP_length:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain at most " + most_acceptable_OTP_length + " characters."})
        return value
