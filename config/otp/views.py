from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .CustomOTPManager import CustomAccountVerificationOTPManager, CustomNewPhoneNumberVerificationOTPManager, CustomForgetPasswordOTPManager, CustomForgetPasswordOTPManager
from .serializers import OTPVerifierSerializer
from .models import OTPCode
from django.contrib.auth import get_user_model
# Create your views here.


UserModel = get_user_model()



class validateAccountVerificationOTP(GenericAPIView, CustomAccountVerificationOTPManager):
    permission_classes = [AllowAny]
    serializer_class = OTPVerifierSerializer
    queryset = OTPCode.objects.all()

        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = UserModel.objects.get(pk=validated_data['pk'])
        return self.verifyOTP(user, 'timer_based', 'account_verification', validated_data['otp'])



class validateNewPhoneNumberVerificationOTP(GenericAPIView, CustomNewPhoneNumberVerificationOTPManager):
    permission_classes = [AllowAny]
    serializer_class = OTPVerifierSerializer
    queryset = OTPCode.objects.all()

        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = UserModel.objects.get(pk=validated_data['pk'])
        return self.verifyOTP(user, 'new_phone_number_verification', validated_data['otp'])

