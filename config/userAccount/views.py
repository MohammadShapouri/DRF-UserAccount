from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import UserAccount
from .permissions import ISOwnerOrAdmin
from .serializers import UserAccountCreationSerializer, UserAccountUpdationSerializer, UserAccountRetrivalSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserAccountDeletionSerializer
from django.db.models import Q
from .userAccountOTPManager import UserAccountOTPManager, UserAccountVerificationOTPManager, UserAccountNewPhoneNumberVerificationOTPManager
from rest_framework.response import Response
from rest_framework import status
from otp.views import VerifyUserAccountVerificationOTPView, VerifyNewPhoneNumberVerificationOTPView
# Create your views here.



class UserAccountViewSet(ModelViewSet, UserAccountOTPManager):
    # queryset = UserAccount.objects.all()
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            self.queryset = UserAccount.objects.all()
        else:
            self.queryset = UserAccount.objects.filter(Q(is_active=True) & Q(is_account_verified=True))
        return super().get_queryset()


    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            pk = self.kwargs['pk']
        except KeyError:
            pk = None
        context.update({'user': self.request.user, 'requested_pk': pk})
        return context
    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserAccountRetrivalSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserAccountUpdationSerializer
        elif self.request.method == 'POST':
            return UserAccountCreationSerializer
        elif self.request.method == 'DELETE':
            return UserAccountDeletionSerializer
        return super().get_serializer_class()


    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [ISOwnerOrAdmin]
        elif self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'DELETE':
            self.permission_classes = [ISOwnerOrAdmin]
        return super().get_permissions()
    

    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save()
        else:
            user = serializer.save(is_active=False, is_account_verified=False)
            OTP = self.generateOTP(user = user,
                                    OTPConfigName = 'account_verification'
                                    )
            serializer.data['account_verification'] = "For verifing your account, Please check you SMS."
            print(OTP.otp)



    def perform_update(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save()
        else:
            if serializer.validated_data['phone_number'] != serializer.instance.phone_number:
                newPhoneNumber = serializer.validated_data['phone_number']
                serializer.validated_data['phone_number'] = serializer.instance.phone_number
                user = serializer.save(new_phone_number=newPhoneNumber, is_new_phone_verified=False)
                OTP = self.generateOTP(user = user,
                                        OTPConfigName = 'new_phone_number_verification'
                                        )
                serializer.data['new_phone_number_verification'] = "For verifing your new phone number, Please check you SMS."
            else:
                serializer.save()


    def perform_destroy(self, instance):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return super().perform_destroy(instance)



class CustomVerifyUserAccountVerificationOTPView(VerifyUserAccountVerificationOTPView, UserAccountVerificationOTPManager):
    def OTPVerifier(self, user, OTPConfigName, OTPCode):
        return self.verifyOTP(user, OTPConfigName, OTPCode)


class CustomVerifyNewPhoneNumberVerificationOTPView(VerifyNewPhoneNumberVerificationOTPView, UserAccountNewPhoneNumberVerificationOTPManager):
    def OTPVerifier(self, user, OTPConfigName, OTPCode):
        return self.verifyOTP(user, OTPConfigName, OTPCode)

