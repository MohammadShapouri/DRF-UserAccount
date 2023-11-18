from django.urls import path
from . import views
from rest_framework import routers


router = routers.SimpleRouter()
router.register('users', views.UserAccountViewSet, basename='UserAccount')

urlpatterns = [
    path('otp/<int:userPk>/verify-account', views.CustomVerifyUserAccountVerificationOTPView.as_view(), name='Verify Account'),
    path('otp/<int:userPk>/verify-new-phone-number', views.CustomVerifyNewPhoneNumberVerificationOTPView.as_view(), name='Verify New Phone Number'),
]
urlpatterns += router.urls