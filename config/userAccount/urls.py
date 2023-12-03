from django.urls import path
from . import views
from rest_framework import routers



router = routers.SimpleRouter()
router.register('users', views.UserAccountViewSet, basename='UserAccount')





userAccountProfilePictureViewSet_list = views.UserAccountProfilePictureViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
userAccountProfilePictureViewSet_detail = views.UserAccountProfilePictureViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

userAccountProfilePictureViewSet_urlpatterns = [
    path('users/<int:userPK>/profile-pictures/', userAccountProfilePictureViewSet_list, name='UserAccountProfilePicture-list'),
    path('users/<int:userPK>/profile-pictures/<int:picturePK>', userAccountProfilePictureViewSet_detail, name='UserAccountProfilePicture-detail')
]





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
    # Resend New New PhoneNumber Verification OTP URL.
    path('users/<int:userPK>/resend-new-phone-number-verification-otp', views.ResendNewNewPhoneNumberVerificationOTPView.as_view(), name='Resend New New PhoneNumber Verification OTP')
]
urlpatterns += router.urls
urlpatterns += userAccountProfilePictureViewSet_urlpatterns
