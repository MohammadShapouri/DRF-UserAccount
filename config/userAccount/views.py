from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import UserAccount, UserAccountProfilePicture
from .permissions import IsOwnerOrAdmin, IsPictureOwnerOrAdmin
from .serializers import UserAccountCreationSerializer, UserAccountUpdateSerializer, UserAccountRetrivalSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserAccountDeletionSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .models import UserAccount
from .permissions import IsOwnerOrAdmin, IsOwner
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser
from otp.views import VerifyUserAccountVerificationOTPView, VerifyNewPhoneNumberVerificationOTPView
from .tasks import send_SMS
from .user_account_OTP_manager import (
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
                        verifyResetPasswordOTPSerializer,
                        UserAccountProfilePictureSerializer
                        )
# Create your views here.


class NoExistingUser(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {"detail": "No user account found."}
    default_code = 'no user'


class NoExistingOTPCodeObject(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {'detail': "OTP code does not exist."}
    default_code = 'no otp code object'


class InactiveUser(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "Account is not active."}
    default_code = 'inactive user'


class NoExistingUserForProfilePhoto(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"detail": "No user account with this id added profile photo."}
    default_code = 'inactive user'




class UserAccountViewSet(ModelViewSet, UserAccountOTPManager):
    queryset = UserAccount.objects.all()
    lookup_url_kwarg = 'userPK'

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            self.queryset = UserAccount.objects.all()
        else:
            self.queryset = UserAccount.objects.filter(Q(is_active=True) & Q(is_account_verified=True))
        return super().get_queryset()


    def get_object(self):
        queryset = self.filter_queryset(self.queryset)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = None
        obj = None
        # get_queryset returns lists. for managing lists, no action required here.
        # For working with specific objects, the following part handles its logic.
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except UserAccount.DoesNotExist:
            raise NoExistingUser
        self.check_object_permissions(self.request, obj)
        
        if (self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff) or (obj.is_active == True and obj.is_account_verified == True):
            return obj
        else:
            raise InactiveUser


    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            pk = self.kwargs['pk']
        except KeyError:
            pk = None
        context.update({'user': self.request.user, 'requested_pk': pk})
        return context


    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserAccountUpdateSerializer
        elif self.request.method == 'POST':
            return UserAccountCreationSerializer
        elif self.request.method == 'DELETE':
            return UserAccountDeletionSerializer
        else:
            return UserAccountRetrivalSerializer
        return super().get_serializer_class()


    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsOwnerOrAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


    def perform_create(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save()
        else:
            user = serializer.save(is_active=False, is_account_verified=False)
            OTP = self.generate_OTP(user = user,
                                    OTP_config_name = 'account_verification'
                                    )
            serializer.data['account_verification'] = "For verifing your account, Please check you SMS."
            send_SMS.delay(OTP.otp)


    def perform_update(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save()
        else:
            if serializer.validated_data['phone_number'] != serializer.instance.phone_number:
                new_phone_number = serializer.validated_data['phone_number']
                serializer.validated_data['phone_number'] = serializer.instance.phone_number
                user = serializer.save(new_phone_number=new_phone_number, is_new_phone_verified=False)
                OTP = self.generate_OTP(user = user,
                                        OTP_config_name = 'new_phone_number_verification'
                                        )
                serializer.data['new_phone_number_verification'] = "For verifing your new phone number, Please check you SMS."
            else:
                serializer.save()


    def perform_destroy(self, instance):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return super().perform_destroy(instance)





class UserAccountChangePasswordView(GenericAPIView):
    lookup_url_kwarg = 'userPK'
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsOwner]
    userObject = None

    def get_object(self):
        userObject = None
        try:
            userPK = self.kwargs[self.lookup_url_kwarg]
            userObject = UserAccount.objects.get(pk=userPK)
        except UserAccount.DoesNotExist:
            raise NoExistingUser
        
        self.check_object_permissions(self.request, userObject)
        if userObject.is_active == True and userObject.is_account_verified == True:
            return userObject
        else:
            raise InactiveUser


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.userObject})
        return context


    def post(self, request, *args, **kwargs):
        self.userObject = self.get_object()
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
        # Only generates and sends OTP code to existing accounts which are active.
        if userObject != None:
            OTP = self.generate_OTP(userObject, 'reset_password')
            send_SMS.delay(OTP.otp)
        return Response({'detail': "Reset password token will be sent to your phone number."}, status.HTTP_200_OK)





class verifyResetPasswordOTP(GenericAPIView, UserAccountOTPManager):
    serializer_class = verifyResetPasswordOTPSerializer
    permission_classes = [AllowAny]
    OTPInputCode = None

    def get_object(self):
        OTP_code_object = self.get_OTP_model_object_by_user_input_code(self.OTPInputCode, 'reset_password')
        if OTP_code_object == None:
            raise NoExistingOTPCodeObject
        else:
            return OTP_code_object


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.OTPInputCode = serializer.validated_data['otp']
        OTP_code_object = self.get_object()
        if OTP_code_object.user.is_active == True and OTP_code_object.user.is_account_verified == True:
            return Response({'detail': "OTP code exists."}, status.HTTP_200_OK)
        else:
            return Response({'detail': "OTP code exists but related account to this OTP code is not active."}, status.HTTP_403_FORBIDDEN)





class ResetPasswordView(GenericAPIView, ResetPasswordOTPManager):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': "Account password reseted successfully."}, status.HTTP_200_OK)





class ResendNewNewPhoneNumberVerificationOTPView(GenericAPIView, UserAccountOTPManager):
    lookup_url_kwarg = 'userPK'
    permission_classes = [IsOwner]

    def get_object(self):
        userObject = None
        try:
            userPK = self.kwargs[self.lookup_url_kwarg]
            userObject = UserAccount.objects.get(pk=userPK)
        except UserAccount.DoesNotExist:
            raise NoExistingUser
    
        self.check_object_permissions(self.request, userObject)
        if userObject.is_active == True and userObject.is_account_verified == True:
            return userObject
        else:
            raise InactiveUser


    def post(self, request, *args, **kwargs):
        userObject = self.get_object()
        if userObject.is_new_phone_verified == False and userObject.new_phone_number != None:
            OTP = self.generate_OTP(userObject, 'new_phone_number_verification')
            send_SMS.delay(OTP.otp)
            return Response({"detail": "New phone number verification OTP will be sent."}, status.HTTP_200_OK)
        else:
            return Response({"detail": "You don't have new phone number to verify."}, status.HTTP_200_OK)









class CustomVerifyUserAccountVerificationOTPView(VerifyUserAccountVerificationOTPView, UserAccountVerificationOTPManager):
    def OTPVerifier(self, user, OTP_config_name, OTPCode):
        return self.verify_OTP(user, OTP_config_name, OTPCode)





class CustomVerifyNewPhoneNumberVerificationOTPView(VerifyNewPhoneNumberVerificationOTPView, UserAccountNewPhoneNumberVerificationOTPManager):
    def OTPVerifier(self, user, OTP_config_name, OTPCode):
        return self.verify_OTP(user, OTP_config_name, OTPCode)





class UserAccountProfilePictureViewSet(ModelViewSet):
    serializer_class = UserAccountProfilePictureSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsPictureOwnerOrAdmin]
    lookup_url_kwarg = 'picturePK'


    def get_queryset(self):
        userPK = self.kwargs.get('userPK')
        self.queryset = UserAccountProfilePicture.objects.filter(user__pk=userPK)
        if len(self.queryset) == 0:
            raise NoExistingUserForProfilePhoto

        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            pass
        else:
            if self.queryset[0].user.is_active == False and self.queryset[0].user.is_account_verified == False:
                raise InactiveUser
        return super().get_queryset()


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request,
                        # 'user': self.request.user
                        })
        return context
    

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [IsPictureOwnerOrAdmin]
        elif self.request.method == 'POST':
            self.permission_classes = [IsPictureOwnerOrAdmin]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsPictureOwnerOrAdmin]
        return super().get_permissions()
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.is_staff:
                serializer.save()
            else:
                if self.kwargs.get('userPK') == self.request.user.pk:
                    serializer.save(user=self.request.user)
                else:
                    return Response({'detail': "You can't add profile picture to other user accounts."}, status=status.HTTP_403_FORBIDDEN)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': "You don't have access to add profile picture. Please login first."}, status=status.HTTP_403_FORBIDDEN)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            self.perform_update(serializer)
        else:
            if instance.is_default_pic == False:
                serializer.save(is_default_pic=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
