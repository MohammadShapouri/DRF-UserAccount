from django.urls import path
from . import views


urlpatterns = [
    path('<int:userPk>/verify-account', views.VerifyUserAccountVerificationOTPView.as_view(), name='Verify Account'),
    path('/<int:userPk>/verify-new-phone-number', views.VerifyNewPhoneNumberVerificationOTPView.as_view(), name='Verify New Phone Number'),
]