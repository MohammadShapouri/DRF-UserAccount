from django.db import models
from django.utils import timezone
from hashlib import sha256
from django.db.utils import OperationalError, ProgrammingError
from django.conf import settings
import string
import random
# Create your models here.


class OTPTypeSettingManager(models.Manager):
    def delete_invalid_records(self):
        otp_type_availability_dict = {'timer_counter_based': False, 'counter_based': False, 'timer_based': False}
        try:
            for each_otp_type_setting in OTPTypeSetting.objects.all():
                if each_otp_type_setting.otp_type in list(otp_type_availability_dict.keys()) and otp_type_availability_dict[each_otp_type_setting.otp_type] == False:
                    otp_type_availability_dict[each_otp_type_setting.otp_type] = True
                else:
                    each_otp_type_setting.delete()
        except OperationalError as e:
            if settings.DEBUG == True:
                raise e
            else:
                print("OperationalError Raised.")
        except ProgrammingError:
            if settings.DEBUG == True:
                raise e
            else:
                print("ProgrammingError Raised.")



    def create_otp_types(self):
        try:
            otp_type_setting = OTPTypeSetting.objects.all()

            if len(otp_type_setting) == 0:
                OTPTypeSetting.objects.bulk_create(
                    [
                        OTPTypeSetting(otp_type='timer_counter_based', max_attempt_count=3, expire_after=180),
                        OTPTypeSetting(otp_type='counter_based', max_attempt_count=3, expire_after=0),
                        OTPTypeSetting(otp_type='timer_based', max_attempt_count=0, expire_after=180),
                    ]
                )
            else:
                otp_type_availability_dict = {'timer_counter_based': False, 'counter_based': False, 'timer_based': False}
                for each_otp_type_setting in otp_type_setting:
                    if each_otp_type_setting.otp_type in list(otp_type_availability_dict.keys()) and otp_type_availability_dict[each_otp_type_setting.otp_type] == False:
                        otp_type_availability_dict[each_otp_type_setting.otp_type] = True
                
                for key, value in otp_type_availability_dict.items():
                    if value == False:
                        if key == 'timer_counter_based':
                            OTPTypeSetting.objects.create(otp_type='timer_counter_based', max_attempt_count=3, expire_after=180)
                        elif key == 'counter_based':
                            OTPTypeSetting.objects.create(otp_type='counter_based', max_attempt_count=3, expire_after=0)
                        elif key == 'timer_based':
                            OTPTypeSetting.objects.create(otp_type='timer_based', max_attempt_count=0, expire_after=180)
        except OperationalError as e:
            if settings.DEBUG == True:
                raise e
            else:
                print("OperationalError Raised.")
        except ProgrammingError:
            if settings.DEBUG == True:
                raise e
            else:
                print("ProgrammingError Raised.")


    def define_settings(self):
        self.delete_invalid_records()
        self.create_otp_types()





class OTPTypeSetting(models.Model):
    OTP_TYPE_CHOICES = (
        ('timer_counter_based', 'Both Timer and Counter Based'),
        ('counter_based', 'Counter Based'),
        ('timer_based', 'Timer Based')
    )
    otp_type            = models.CharField(choices=OTP_TYPE_CHOICES, max_length=19, blank=False, null=False, verbose_name='OTP Type')
    max_attempt_count   = models.IntegerField(default=3, blank=False, null=False, verbose_name='Max Possible Attempt Number (For "Counter Based" and "Both Timer and Counter Based" OTPs)')
    expire_after        = models.IntegerField(default=180, blank=False, null=False, verbose_name='Expire OTP After (Seconds) [For "Timer Based" and "Both Timer and Counter Based" OTPs]')
    creation_date       = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    update_date         = models.DateTimeField(auto_now=True, verbose_name='Update Date')

    objects = OTPTypeSettingManager()

    class Meta:
        verbose_name = 'OTP Type and Setting'
        verbose_name_plural = 'OTP Types and Settings'


    def __str__(self):
        return str(self.otp_type)





class OTPCodeManager(models.Manager):
    def create_otp(self, otp_type_setting, otp_usage, otp_length=5):
        allowedChars = string.digits
        otp_code = ''.join(random.choices(allowedChars, k=otp_length))
        otp_obj = OTPCode.objects.create(otp_code=sha256(str(otp_code).encode('utf-8')).hexdigest(), otp_usage=otp_usage, otp_type_setting=otp_type_setting)
        return otp_code, otp_obj

def define_otp_usage_choices():
    try:
        return settings.OTP_USAGE_CHOICES
    except AttributeError:
        return (
            ('activate_account', 'Account Activation OTP'),
            ('verify_login', 'Login Verification OTP'),
            ('reset_password', 'Password Reset OTP'),
            ('update_account', 'Account Update Verification OTP'),
            ('delete_account', 'Account Delete Verification OTP'),
            ('general_verification', 'General Verification (For Shopping, etc...)'),
        )

class OTPCode(models.Model):
    otp_code            = models.CharField(max_length=200, blank=False, null=False, verbose_name='One Time Password Code')
    otp_usage           = models.CharField(choices=define_otp_usage_choices(), max_length=20, blank=False, null=False, verbose_name='OTP Usage')
    otp_type_setting    = models.ForeignKey('OTPTypeSetting', blank=False, null=False, on_delete=models.CASCADE, verbose_name="OTP Type and Setting")
    otp_creation_date   = models.DateTimeField(auto_now_add=True, verbose_name='OTP Code Creation Date')
    attempt_counter     = models.PositiveIntegerField(default=0, verbose_name='Number of Attempts')
    last_attempt        = models.DateTimeField(auto_now=True, verbose_name='Last Attempt')

    objects = OTPCodeManager()

    class Meta:
        verbose_name = 'OTP Code'
        verbose_name_plural = 'OTP Codes'


    def __str__(self):
        return str(self.otp_usage) + ' - ' + str(self.otp_type_setting)


    def can_attempt(self):
        if self.attempt_counter < self.otp_type_setting.max_attempt_count:
            return True
        return False
    

    def has_time(self):
        if self.otp_creation_date + timezone.timedelta(seconds=self.otp_type_setting.expire_after) > timezone.now():
            return True
        return False


    def increment_attempt_counter_value(self):
        self.attempt_counter = self.attempt_counter + 1
        self.save()



    def check_otp(self, otp_code, otp_usage, delete_otp_object=False):
            if self.__class__.__name__ != 'OTPCode':
                if settings.DEBUG == True:
                    raise ValueError()
                else:
                    return False, 'error', "ValueError Raised. Object must be an instance of 'OTPCode' class."

            if self.otp_usage == otp_usage:
                if self.otp_type_setting.otp_type == 'timer_based':
                    if self.has_time():
                        if self.otp_code == sha256(str(otp_code).encode('utf-8')).hexdigest():
                            if delete_otp_object:
                                self.delete()
                            return True, None, None
                        else:
                            return False, 'wrong_opt_code', None
                    else:
                        return False, 'expired', None
                elif self.otp_type_setting.otp_type == 'counter_based':
                    if self.can_attempt():
                        if self.otp_code == sha256(otp_code.encode('utf-8')).hexdigest():
                            if delete_otp_object:
                                self.delete()
                            return True, None, None
                        else:
                            self.increment_attempt_counter_value()
                            return False, 'wrong_opt_code', None
                    else:
                        return False, 'max_attempt_exceeded', None
                elif self.otp_type_setting.otp_type == 'timer_counter_based':
                    if self.has_time():
                        if self.can_attempt():
                            if self.otp_code == sha256(otp_code.encode('utf-8')).hexdigest():
                                if delete_otp_object:
                                    self.delete()
                                return True, None, None
                            else:
                                self.increment_attempt_counter_value()
                                return False, 'wrong_opt_code', None
                        else:
                            return False, 'max_attempt_exceeded', None
                    else:
                        return False, 'expired', None
                else:
                    return False, f'structure_error', "OTP types can be '', '' or ''. {self.otp_type_setting.otp_type} is invalid."
            else:
                return False, 'different_otp_usage', None 

