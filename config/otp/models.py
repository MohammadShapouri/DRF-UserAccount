from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator
# Create your models here.


class OTPCode(models.Model):
    OTP_TYPE_CHOICES = (
        ('timer_counter_based', 'Both Timer and Counter Based'),
        ('counter_based', 'Counter Based'),
        ('timer_based', 'Timer Based')
    )

    # OTP_USAGE_CHOICES = (
    #     ('account_verification', 'Account Verification'),
    #     ('new_phone_number_verification', 'New Phone Number Verification'),
    #     ('forget_password', 'Forgotten Password'),
    #     ('OTP_login', 'ONE Time Password Login')
    # )

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='OTPCode', verbose_name='Related User')
    otp                 = models.CharField(max_length=20, blank=False, null=False, verbose_name="One Time Password Code")
    otp_type            = models.CharField(choices=OTP_TYPE_CHOICES, max_length=19, verbose_name='OTP Type')
    otp_usage           = models.CharField(max_length=50, verbose_name='OTP Usage')
    otp_creation_date   = models.DateTimeField(auto_now_add=True, verbose_name='Currrent OTP Code Creation Date')
    expire_after        = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(30)], verbose_name='Expire After (Seconds)')
    try_counter         = models.PositiveIntegerField(default=0, verbose_name='Number of Attempts')
    max_possible_try    = models.PositiveIntegerField(validators=[MinValueValidator(3)], verbose_name='Maximum possible number of Attempts')
    last_try            = models.DateTimeField(auto_now=True, verbose_name='Last Attempt')
    need_recreation     = models.BooleanField(default=False, verbose_name='Does User Need New OTP Code?')


    class Meta:
        verbose_name = 'OTP Code'
        verbose_name_plural = 'OTP Codes'


    def __str__(self):
        return str(self.user) + ' -- ' + str(self.otp_usage)
    

    def canTry(self):
        if self.try_counter < self.max_possible_try:
            return True
        return False
    

    def hasTime(self):
        if self.otp_creation_date + timezone.timedelta(seconds=self.expire_after) > timezone.now():
            return True
        return False


    def incrementTryCounterValue(self):
        self.try_counter += 1
        self.save()
