from django.urls import path
from . import views
from rest_framework import routers


router = routers.SimpleRouter()
router.register('users', views.UserAccountViewSet, basename='UserAccount')

urlpatterns = [
    # Change password URL.
    path('users/<int:userPK>/change-password', views.UserAccountChangePasswordView.as_view(), name='Change Password'),
    # Reset password URLs.
    path('users/request-reset-password-otp', views.RequestResetPasswordOTP.as_view(), name='Request ResetPassword OTP'),
    path('users/verify-reset-password-otp', views.verifyResetPasswordOTP.as_view(), name='Verify Reset Password OTP'),
    path('users/reset-password', views.ResetPasswordView.as_view(), name='Reset Password'),
    # Verifications password URLs.
    path('users/<int:userPk>/verify-account', views.CustomVerifyUserAccountVerificationOTPView.as_view(), name='Verify Account'),
    path('users/<int:userPk>/verify-new-phone-number', views.CustomVerifyNewPhoneNumberVerificationOTPView.as_view(), name='Verify New Phone Number'),
]
urlpatterns += router.urls
