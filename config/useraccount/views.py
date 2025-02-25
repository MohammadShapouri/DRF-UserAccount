from django.db.models import Q
from .models import UserAccount
from rest_framework import status
from rest_framework.response import Response
from otp.models import OTPCode, OTPTypeSetting
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from extentions.sms_message.sms_sender import send_SMS
from useraccount.models import UserAccountProfilePicture
from .permissions import IsOwnerOrAdmin, IsPictureOwnerOrAdmin, IsOwner
from .exceptions import (
                        NoExistingUser,
                        InactiveUser,
                        NoExistingUserForProfilePhoto
                        )
from useraccount.serializers.generalserializer.serializers import (
                                                                    UserAccountDeletionSerializer,
                                                                    ChangePasswordSerializer,
                                                                    RequestResetPasswordOTPSerializer,
                                                                    VerifyResetPasswordOTPSerializer,
                                                                    ResetPasswordSerializer,
                                                                    VerifyNewPhoneNumberVerificationOTPSerializer,
                                                                    VerifyAccountVerificationOTPSerializer
                                                                    )
from useraccount.serializers.normaluserserializer.serializers import (
                                                                    UserAccountCreationSerializer,
                                                                    UserAccountUpdateSerializer,
                                                                    UserAccountRetrivalSerializer,
                                                                    UserAccountProfilePictureCreationRetrivalSerializer,
                                                                    UserAccountProfilePictureUpdateSerializer
                                                                    )
from useraccount.serializers.superuserserializer.serializers import (
                                                                    UserAccountCreationSerializer as SuperuserUserAccountCreationSerializer,
                                                                    UserAccountUpdateSerializer as SuperuserUserAccountUpdateSerializer,
                                                                    UserAccountRetrivalSerializer as SuperuserUserAccountRetrivalSerializer,
                                                                    UserAccountProfilePictureSerializer as SuperuserUserAccountProfilePictureSerializer
                                                                    )
# Create your views here.


class UserAccountViewSet(ModelViewSet):
    queryset = UserAccount.objects.all()
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
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
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = queryset.get(**filter_kwargs)
        except UserAccount.DoesNotExist:
            raise NoExistingUser
        self.check_object_permissions(self.request, obj)

        if (self.request.user.is_authenticated and self.request.user.is_superuser) or (obj.is_active == True and obj.is_account_verified == True):
            return obj
        else:
            raise InactiveUser


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        if self.request.method != 'POST':
            context.update({'requested_user': self.get_object()})
        return context


    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                return SuperuserUserAccountUpdateSerializer
            elif self.request.method == 'POST':
                return SuperuserUserAccountCreationSerializer
            elif self.request.method == 'DELETE':
                return UserAccountDeletionSerializer
            else:
                return SuperuserUserAccountRetrivalSerializer        
        else:
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                return UserAccountUpdateSerializer
            elif self.request.method == 'POST':
                return UserAccountCreationSerializer
            elif self.request.method == 'DELETE':
                return UserAccountDeletionSerializer
            else:
                return UserAccountRetrivalSerializer  


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
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            serializer.save()
        else:
            user = serializer.save(is_active=False, is_account_verified=False)
            otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'activate_account')
            user.otp_object = otp_object
            user.save()
            send_SMS.delay(otp_code)
            serializer.data['account_verification'] = "For verifing your account, Please check you SMS."


    def perform_update(self, serializer):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            serializer.save()
        else:
            print(serializer.validated_data.get('phone_number', None))
            if serializer.validated_data.get('phone_number', None) != None:
                if serializer.validated_data['phone_number'] != serializer.instance.phone_number:
                    new_phone_number = serializer.validated_data['phone_number']
                    serializer.validated_data['phone_number'] = serializer.instance.phone_number
                    user = serializer.save(new_phone_number=new_phone_number, is_new_phone_verified=False)
                    otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='counter_based'), 'update_account')
                    user.otp_object = otp_object
                    user.save()
                    print(user.is_new_phone_verified)

                    send_SMS.delay(otp_code)
                    serializer.data['new_phone_number_verification'] = "For verifing your new phone number, Please check you SMS."
                    return
            serializer.save()


    def perform_destroy(self, instance):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return super().perform_destroy(instance)





class UserAccountChangePasswordView(GenericAPIView):
    lookup_url_kwarg = 'pk'
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsOwner]
    user_object = None

    def get_object(self):
        try:
            self.user_object = UserAccount.objects.get(pk=self.kwargs[self.lookup_url_kwarg])
        except UserAccount.DoesNotExist:
            raise NoExistingUser
        
        self.check_object_permissions(self.request, self.user_object)
        if self.user_object.is_active == True and self.user_object.is_account_verified == True:
            return self.user_object
        else:
            raise InactiveUser


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.user_object})
        return context


    def post(self, request, *args, **kwargs):
        self.user_object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status.HTTP_200_OK)





class RequestResetPasswordOTPView(GenericAPIView):
    serializer_class = RequestResetPasswordOTPSerializer
    permission_classes = [AllowAny]
    phone_number = None

    def get_object(self):
        user = None
        try:
            if str(self.phone_number_email_username).find('@') != -1:
                user = UserAccount.objects.get(email__iexact=self.phone_number_email_username)
            else:
                if str(self.phone_number_email_username).isdigit():
                    user = UserAccount.objects.get(phone_number=self.phone_number_email_username)
                else:
                    user = UserAccount.objects.get(username__iexact=self.phone_number_email_username)
        except UserAccount.DoesNotExist:
            return None
        if user.is_active == False and user.is_account_verified == True:
            raise InactiveUser()
        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.phone_number_email_username = serializer.validated_data['phone_number_email_username']
        user = self.get_object()
        # Only generates and sends OTP code to existing accounts which are active.
        if user != None:
            otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'reset_password')
            user.otp_object = otp_object
            send_SMS.delay(otp_code)

        if str(self.phone_number_email_username).isdigit:
            return Response({'detail': "Reset password token will be sent to your phone number."}, status.HTTP_200_OK)
        else:
            return Response({'detail': "Reset password token will be sent to your email."}, status.HTTP_200_OK)





class VerifyResetPasswordOTPView(RequestResetPasswordOTPView):
    serializer_class = VerifyResetPasswordOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        self.phone_number_email_username = serializer.validated_data['phone_number_email_username']
        user = self.get_object()

        if user != None:
            if user.otp_object == None:
                return Response({'OTP': "No OTP code found."}, status.HTTP_404_NOT_FOUND)

            result, error_title, error_desc = user.otp_object.check_otp(otp, 'reset_password')
            if result:
                return self.correct_otp_actions(user, serializer)
            else:
                if error_title == 'wrong_opt_code':
                    return Response({'OTP': "OTP is wrong."}, status.HTTP_200_OK)
                elif error_title == 'max_attempt_exceeded':
                    return Response({'OTP': "Max attempts exceeded for this otp code. request new one"}, status.HTTP_200_OK)
                elif error_title == 'expired':
                    return Response({'OTP': "OTP is expired."}, status.HTTP_200_OK)
                else:
                    return Response({'OTP': error_title}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': "OTP code is wrong."}, status.HTTP_404_NOT_FOUND)


    def correct_otp_actions(self, user, serializer):
        return Response({'OTP': "OTP is correct."}, status.HTTP_200_OK)





class ResetPasswordView(RequestResetPasswordOTPView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def correct_otp_actions(self, user, serializer):
        serializer.save()
        user.otp_object.delete()
        return super().correct_otp_actions(user, serializer)





class RequestNewPhoneNumberVerificationOTPView(GenericAPIView):
    permission_classes = [IsOwner]
    lookup_url_kwarg = 'pk'

    def get_object(self):
        user = None
        try:
            pk = self.kwargs[self.lookup_url_kwarg]
            user = UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return None
        self.check_object_permissions(self.request, user)
        if user.is_active == False and user.is_account_verified == True:
            raise InactiveUser()
        return user


    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user != None:
            if user.is_new_phone_verified == False and user.new_phone_number != None:
                otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='counter_based'), 'update_account')
                user.otp_object = otp_object
                send_SMS.delay(otp_code)

            return Response({"detail": "New phone number verification OTP will be sent."}, status.HTTP_200_OK)
        else:
            return Response({"detail": "You don't have new phone number to verify."}, status.HTTP_400_BAD_REQUEST)





class VerifyNewPhoneNumberVerificationOTPView(GenericAPIView):
    serializer_class = VerifyNewPhoneNumberVerificationOTPSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_url_kwarg = 'pk'

    def get_object(self):
        user = None
        try:
            pk = self.kwargs[self.lookup_url_kwarg]
            user = UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return None
        self.check_object_permissions(self.request, user)
        if user.is_active == False and user.is_account_verified == True:
            raise InactiveUser()
        return user


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        user = self.get_object()

        if user != None:
            if user.otp_object == None:
                return Response({'OTP': "No OTP code found."}, status.HTTP_404_NOT_FOUND)

            result, error_title, error_desc = user.otp_object.check_otp(otp, 'update_account')
            if result:
                return self.correct_otp_actions(user, serializer)
            else:
                if error_title == 'wrong_opt_code':
                    return Response({'OTP': "OTP is wrong."}, status.HTTP_200_OK)
                elif error_title == 'max_attempt_exceeded':
                    return Response({'OTP': "Max attempts exceeded for this otp code. request new one"}, status.HTTP_200_OK)
                elif error_title == 'expired':
                    return Response({'OTP': "OTP is expired."}, status.HTTP_200_OK)
                else:
                    return Response({'OTP': error_title}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': "OTP code is wrong."}, status.HTTP_404_NOT_FOUND)


    def correct_otp_actions(self, user, serializer):
        user.phone_number = user.new_phone_number
        user.new_phone_number = None
        user.is_new_phone_verified = True
        user.save()
        user.otp_object.delete()
        return Response({'OTP': "OTP is correct."}, status.HTTP_200_OK)





class VerifyAccountVerificationOTPView(GenericAPIView):
    serializer_class = VerifyAccountVerificationOTPSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'pk'


    def get_object(self):
        user = None
        try:
            pk = self.kwargs[self.lookup_url_kwarg]
            user = UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return None
        self.check_object_permissions(self.request, user)
        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        user = self.get_object()

        if user != None:
            if user.otp_object == None:
                return Response({'OTP': "No OTP code found."}, status.HTTP_404_NOT_FOUND)

            result, error_title, error_desc = user.otp_object.check_otp(otp, 'activate_account')
            if result:
                return self.correct_otp_actions(user, serializer)
            else:
                if error_title == 'wrong_opt_code':
                    return Response({'OTP': "OTP is wrong."}, status.HTTP_200_OK)
                elif error_title == 'max_attempt_exceeded':
                    return Response({'OTP': "Max attempts exceeded for this otp code. request new one"}, status.HTTP_200_OK)
                elif error_title == 'expired':
                    return Response({'OTP': "OTP is expired."}, status.HTTP_200_OK)
                else:
                    return Response({'OTP': error_title}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': "OTP code is wrong."}, status.HTTP_404_NOT_FOUND)


    def correct_otp_actions(self, user, serializer):
        user.is_active = True
        user.is_account_verified = True
        user.save()
        user.otp_object.delete()
        return Response({'OTP': "OTP is correct. Account verified."}, status.HTTP_200_OK)





class UserAccountProfilePictureViewSet(ModelViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsPictureOwnerOrAdmin]
    lookup_url_kwarg = 'picture_pk'


    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        self.queryset = UserAccountProfilePicture.objects.filter(user__pk=user_pk)
        if len(self.queryset) == 0:
            raise NoExistingUserForProfilePhoto

        if self.request.user.is_authenticated and self.request.user.is_superuser:
            pass
        else:
            if self.queryset[0].user.is_active == False and self.queryset[0].user.is_account_verified == True:
                raise InactiveUser
        return super().get_queryset()


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request,
                        # 'user': self.request.user
                        })
        return context


    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return SuperuserUserAccountProfilePictureSerializer
        else:
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                return UserAccountProfilePictureUpdateSerializer
            else:
                return UserAccountProfilePictureCreationRetrivalSerializer


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
            if self.request.user.is_superuser:
                serializer.save()
            else:
                if self.kwargs.get('user_pk') == self.request.user.pk:
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

        if self.request.user.is_authenticated and self.request.user.is_superuser:
            self.perform_update(serializer)
        else:
            if instance.is_default_pic == False:
                serializer.save(is_default_pic=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
