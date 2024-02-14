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
    path('users/<int:userPK>/change-password', views.UserAccountChangePasswordView.as_view(), name='change-password'),
    # Reset password URLs.
    path('users/request-reset-password-otp', views.RequestResetPasswordOTP.as_view(), name='request-reset-password-OTP'),
    path('users/verify-reset-password-otp', views.verifyResetPasswordOTP.as_view(), name='verify-reset-password-OTP'),
    path('users/reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    # Verifications password URLs.
    path('users/<int:userPK>/verify-account', views.CustomVerifyUserAccountVerificationOTPView.as_view(), name='verify-account'),
    path('users/<int:userPK>/verify-new-phone-number', views.CustomVerifyNewPhoneNumberVerificationOTPView.as_view(), name='verify-new-phone-number'),
    # Resend New New PhoneNumber Verification OTP URL.
    path('users/<int:userPK>/resend-new-phone-number-verification-otp', views.RequestNewNewPhoneNumberVerificationOTPView.as_view(), name='request-new-new-phone-number-verification-OTP')
]
urlpatterns += router.urls
urlpatterns += userAccountProfilePictureViewSet_urlpatterns
