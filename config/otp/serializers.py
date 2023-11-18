from rest_framework import serializers


class OTPVerifierSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['otp'] = serializers.CharField(required=True, label='OTP Code', allow_null=False)


    def validate_otp(self, value):
        if len(value) < 6:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain at least 6 characters."})
        elif str.isdigit(value) is False:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must not contain characters."})
        return value
