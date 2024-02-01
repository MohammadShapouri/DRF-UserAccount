from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .serializers import OTPVerifierSerializer
from .models import OTPCode
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

UserModel = get_user_model()


class VerifyUserAccountVerificationOTPView(GenericAPIView):
    """
    Also inherit your customized OTPManager (or default one if you use default OTPManager) and
    override OTPVerifier and return verify_OTP methods in it to make it usable.
    """
    permission_classes = [AllowAny]
    serializer_class = OTPVerifierSerializer
    queryset = OTPCode.objects.all()
    lookup_field = 'user__pk'
    lookup_url_kwarg = 'userPk'

    validated_data = None
    OTP_code_object = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validated_data = serializer.validated_data
        self.OTP_code_object = self.get_object()
        return self.OTPVerifier(self.OTP_code_object.user, 'account_verification', self.validated_data['otp'])


    def OTPVerifier(self, user, OTP_config_name, OTPCode):
        """
        This method should return a OTPVerifier method.
        """
        pass





class VerifyNewPhoneNumberVerificationOTPView(GenericAPIView):
    """
    Also inherit your customized OTPManager (or default one if you use default OTPManager) and
    override OTPVerifier and return verify_OTP methods in it to make it usable.
    """
    permission_classes = [AllowAny]
    serializer_class = OTPVerifierSerializer
    queryset = OTPCode.objects.all()
    lookup_field = 'user__pk'
    lookup_url_kwarg = 'userPk'

    validated_data = None
    OTP_code_object = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validated_data = serializer.validated_data
        self.OTP_code_object = self.get_object()
        return self.userIsActiveStatusChecker(self.OTP_code_object)
    

    def userIsActiveStatusChecker(self, OTP_code_object):
        if OTP_code_object.user.is_active == True:
            return self.OTPVerifier(OTP_code_object.user, 'new_phone_number_verification', self.validated_data['otp'])
        else:
            return Response({"detail": "Account is not active."}, status.HTTP_403_FORBIDDEN)


    
    def OTPVerifier(self, user, OTP_config_name, OTPCode):
        """
        This method should return a OTPVerifier method.
        """
        pass
