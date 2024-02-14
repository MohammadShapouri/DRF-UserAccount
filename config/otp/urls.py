from django.urls import path
from . import views


urlpatterns = [
    path('<int:userPK>/verify-account', views.VerifyUserAccountVerificationOTPView.as_view(), name='Verify Account'),
    path('/<int:userPK>/verify-new-phone-number', views.VerifyNewPhoneNumberVerificationOTPView.as_view(), name='Verify New Phone Number'),
]