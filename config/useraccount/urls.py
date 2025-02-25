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
    path('users/<int:user_pk>/profile-pictures/', userAccountProfilePictureViewSet_list, name='UserAccountProfilePicture-list'),
    path('users/<int:user_pk>/profile-pictures/<int:picture_pk>', userAccountProfilePictureViewSet_detail, name='UserAccountProfilePicture-detail')
]





urlpatterns = [
    # Change password URL.
    path('users/<int:pk>/change-password', views.UserAccountChangePasswordView.as_view(), name='change-password'),
    # Reset password URLs.
    path('users/request-reset-password-otp', views.RequestResetPasswordOTPView.as_view(), name='request-reset-password-otp'),
    path('users/verify-reset-password-otp', views.VerifyResetPasswordOTPView.as_view(), name='verify-reset-password-otp'),
    path('users/reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    # Verifications password URLs.
    path('users/<int:pk>/verify-account', views.VerifyAccountVerificationOTPView.as_view(), name='verify-account'),
    path('users/<int:pk>/verify-new-phone-number', views.VerifyNewPhoneNumberVerificationOTPView.as_view(), name='verify-new-phone-number'),
    # Resend New New PhoneNumber Verification OTP URL.
    path('users/<int:pk>/resend-new-phone-number-verification-otp', views.RequestNewPhoneNumberVerificationOTPView.as_view(), name='request-new-new-phone-number-verification-otp')
]
urlpatterns += router.urls
urlpatterns += userAccountProfilePictureViewSet_urlpatterns
