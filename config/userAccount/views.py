from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import UserAccount
from .permissions import ISOwnerOrAdmin
from .serializers import UserAccountCreationSerializer, UserAccountUpdateSerializer, UserAccountRetrivalSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserAccountDeletionSerializer
from django.db.models import Q
from .userAccountOTPManager import UserAccountOTPManager, UserAccountVerificationOTPManager, UserAccountNewPhoneNumberVerificationOTPManager
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount
from .permissions import ISOwnerOrAdmin, IsOwner
from django.db.models import Q
from otp.views import VerifyUserAccountVerificationOTPView, VerifyNewPhoneNumberVerificationOTPView
from .userAccountOTPManager import (
                                    UserAccountOTPManager,
                                    UserAccountVerificationOTPManager,
                                    UserAccountNewPhoneNumberVerificationOTPManager,
                                    ResetPasswordOTPManager
                                    )
from .serializers import (
                        UserAccountCreationSerializer,
                        UserAccountUpdateSerializer,
                        UserAccountRetrivalSerializer,
                        UserAccountDeletionSerializer,
                        ChangePasswordSerializer,
                        ResetPasswordSerializer,
                        RequestResetPasswordOTPSerializer,
                        verifyResetPasswordOTPSerializer
                        )
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
            return UserAccountUpdateSerializer
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





class UserAccountChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsOwner]
    userObject = None
    lookup_url_kwarg = 'userPK'

    def get_object(self):
        try:
            pk = self.kwargs[self.lookup_url_kwarg]
        except KeyError:
            self.userObject = None
            return

        try:
            self.userObject = UserAccount.objects.get(Q(pk=pk) & Q(is_active=True) & Q(is_account_verified=True))
        except UserAccount.DoesNotExist:
            self.userObject = None
            return
        self.check_object_permissions(self.request, self.userObject)


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.userObject})
        return context

    def post(self, request, *args, **kwargs):
        self.get_object()
        if self.userObject == None:
            return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Password changed successfully."}, status.HTTP_200_OK)





class RequestResetPasswordOTP(GenericAPIView, UserAccountOTPManager):
    serializer_class = RequestResetPasswordOTPSerializer
    permission_classes = [AllowAny]
    phoneNumber = None

    def get_object(self):
        try:
            return UserAccount.objects.get(Q(phone_number=self.phoneNumber) & Q(is_active=True) & Q(is_account_verified=True))
        except UserAccount.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.phoneNumber = serializer.validated_data['phone_number']
        userObject = self.get_object()
        if userObject != None:
            OTP = self.generateOTP(userObject, 'reset_password')
            print(OTP.otp)
        return Response({'detail': "Reset password token will be sent to your phone number."}, status.HTTP_200_OK)





class verifyResetPasswordOTP(GenericAPIView, UserAccountOTPManager):
    serializer_class = verifyResetPasswordOTPSerializer
    permission_classes = [AllowAny]
    OTPInputCode = None
    OTPCodeObject = None

    def get_object(self):
        self.OTPCodeObject = self.getOTPModelObject(self.OTPInputCode, 'reset_password')
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.OTPInputCode = serializer.validated_data['otp']
        self.get_object()
        if self.OTPCodeObject == None:
            return Response({'detail': "OTP code does not exist."}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': "OTP code exists."}, status.HTTP_200_OK)





class ResetPasswordView(GenericAPIView, ResetPasswordOTPManager):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': "Account password reseted successfully."}, status.HTTP_200_OK)





class CustomVerifyUserAccountVerificationOTPView(VerifyUserAccountVerificationOTPView, UserAccountVerificationOTPManager):
    def OTPVerifier(self, user, OTPConfigName, OTPCode):
        return self.verifyOTP(user, OTPConfigName, OTPCode)





class CustomVerifyNewPhoneNumberVerificationOTPView(VerifyNewPhoneNumberVerificationOTPView, UserAccountNewPhoneNumberVerificationOTPManager):
    def OTPVerifier(self, user, OTPConfigName, OTPCode):
        return self.verifyOTP(user, OTPConfigName, OTPCode)
