from otp.models import OTPCode, OTPTypeSetting, define_otp_usage_choices
from django.conf import settings
from django.test import TestCase
from hashlib import sha256
import time
# Create your tests here.



class UserAccountTests(TestCase):
    maxDiff = None

    def setUp(self):
        # Setup run before every test method.
        OTPTypeSetting.objects.create(otp_type='invalid_type_1', max_attempt_count=0, expire_after=180)
        OTPTypeSetting.objects.create(otp_type='invalid_type_2', max_attempt_count=5, expire_after=180)
        OTPTypeSetting.objects.create(otp_type='invalid_type_3', max_attempt_count=5, expire_after=0)


    def tearDown(self):
        # Clean up run after every test method.
        pass


    def test_otp_type_setting_delete_invalid_records(self):
        self.assertEqual(len(OTPTypeSetting.objects.all()), 3)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='timer_counter_based')), 0)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='counter_based')), 0)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='timer_based')), 0)
        OTPTypeSetting.objects.delete_invalid_records()
        self.assertEqual(len(OTPTypeSetting.objects.all()), 0)


    def test_otp_type_setting_create_otp_types_1(self):
        OTPTypeSetting.objects.delete_invalid_records()
        self.assertEqual(len(OTPTypeSetting.objects.all()), 0)
        OTPTypeSetting.objects.create_otp_types()
        self.assertEqual(len(OTPTypeSetting.objects.all()), 3)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='timer_counter_based')), 1)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='counter_based')), 1)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='timer_based')), 1) 


    def test_otp_type_setting_create_otp_types_2(self):
        OTPTypeSetting.objects.create(otp_type='counter_based', max_attempt_count=3, expire_after=0),
        OTPTypeSetting.objects.delete_invalid_records()
        self.assertEqual(len(OTPTypeSetting.objects.all()), 1)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='counter_based')), 1)
        OTPTypeSetting.objects.create_otp_types()
        self.assertEqual(len(OTPTypeSetting.objects.all()), 3)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='timer_counter_based')), 1)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='counter_based')), 1)
        self.assertEqual(len(OTPTypeSetting.objects.filter(otp_type='timer_based')), 1) 


    def test_define_otp_usage_choices_1(self):
        settings.__setattr__('OTP_USAGE_CHOICES', (('choice_1','verbose name 1'), ('choice_2','verbose name 2')))
        res = define_otp_usage_choices()
        self.assertEqual(len(res), 2)
        self.assertTupleEqual(res ,(('choice_1','verbose name 1'), ('choice_2','verbose name 2')))


    def test_define_otp_usage_choices_2(self):
        settings.__delattr__('OTP_USAGE_CHOICES')
        res = define_otp_usage_choices()
        self.assertEqual(len(res), 6)
        self.assertTupleEqual(res ,(
            ('activate_account', 'Account Activation OTP'),
            ('verify_login', 'Login Verification OTP'),
            ('reset_password', 'Password Reset OTP'),
            ('update_account', 'Account Update Verification OTP'),
            ('delete_account', 'Account Delete Verification OTP'),
            ('general_verification', 'General Verification (For Shopping, etc...)'),
        ))


    def test_create_otp_1(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        self.assertEqual(len(OTPCode.objects.all()), 0)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'activate_account', 8)
        self.assertEqual(len(OTPCode.objects.all()), 1)
        self.assertEqual(len(OTPCode.objects.filter(otp_usage='activate_account')), 1)
        self.assertEqual(len(str(otp_code)), 8)
        self.assertEqual(len(OTPCode.objects.filter(otp_type_setting=OTPTypeSetting.objects.get(otp_type='timer_counter_based'))), 1)
        self.assertEqual(otp_object.otp_code, sha256(str(otp_code).encode('utf-8')).hexdigest())


    def test_create_otp_2(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        self.assertEqual(len(OTPCode.objects.all()), 0)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'activate_account')
        self.assertEqual(len(OTPCode.objects.all()), 1)
        self.assertEqual(len(OTPCode.objects.filter(otp_usage='activate_account')), 1)
        self.assertEqual(len(str(otp_code)), 5)
        self.assertEqual(len(OTPCode.objects.filter(otp_type_setting=OTPTypeSetting.objects.get(otp_type='timer_counter_based'))), 1)
        self.assertEqual(otp_object.otp_code, sha256(str(otp_code).encode('utf-8')).hexdigest())


    def test_invalid_otp_type_check_otp(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        OTPTypeSetting.objects.create(otp_type='invalid_type', max_attempt_count=5, expire_after=0)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='invalid_type'), 'activate_account', 8)
        result, msg, desc = otp_object.check_otp(otp_code, 'activate_account')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'structure_error')


    def test_invalid_otp_type_usage_otp(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_based'), 'activate_account', 8)
        result, msg, desc = otp_object.check_otp(otp_code, 'invalid_usage')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'different_otp_usage')


    def test_different_otp_type_usage_otp(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_based'), 'different_usage', 8)
        result, msg, desc = otp_object.check_otp(otp_code, 'different_usage')
        self.assertEqual(result, True)
        self.assertEqual(msg, None)


    def test_counter_based_check_otp_1(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='counter_based'), 'general_verification', 8)

        for i in range(OTPTypeSetting.objects.get(otp_type='counter_based').max_attempt_count):
            result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
            self.assertEqual(result, False)
            self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'max_attempt_exceeded')


    def test_counter_based_check_otp_2(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='counter_based'), 'general_verification', 8)

        for i in range(OTPTypeSetting.objects.get(otp_type='counter_based').max_attempt_count-1):
            result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
            self.assertEqual(result, False)
            self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
        self.assertEqual(result, True)
        self.assertEqual(msg, None)


    def test_timer_based_check_otp_1(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_type_setting_obj = OTPTypeSetting.objects.get(otp_type='timer_based')
        otp_type_setting_obj.expire_after = 3
        otp_type_setting_obj.max_attempt_count = 0
        otp_type_setting_obj.save()
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_based').max_attempt_count, 0)
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_based').expire_after, 3)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_based'), 'general_verification')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        time.sleep(3)
        result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'expired')


    def test_timer_based_check_otp_2(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_type_setting_obj = OTPTypeSetting.objects.get(otp_type='timer_based')
        otp_type_setting_obj.expire_after = 5
        otp_type_setting_obj.max_attempt_count = 0
        otp_type_setting_obj.save()
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_based').max_attempt_count, 0)
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_based').expire_after, 5)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_based'), 'general_verification')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
        self.assertEqual(result, True)
        self.assertEqual(msg, None)


    def test_timer_counter_based_check_otp_1(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_type_setting_obj = OTPTypeSetting.objects.get(otp_type='timer_counter_based')
        otp_type_setting_obj.expire_after = 5
        otp_type_setting_obj.max_attempt_count = 5
        otp_type_setting_obj.save()
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_counter_based').max_attempt_count, 5)
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_counter_based').expire_after, 5)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'general_verification')

        for i in range(OTPTypeSetting.objects.get(otp_type='timer_counter_based').max_attempt_count):
            result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
            self.assertEqual(result, False)
            self.assertEqual(msg, 'wrong_opt_code')

        result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
        self.assertEqual(result, False)
        self.assertEqual(msg, 'max_attempt_exceeded')


    def test_timer_counter_based_check_otp_2(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_type_setting_obj = OTPTypeSetting.objects.get(otp_type='timer_counter_based')
        otp_type_setting_obj.expire_after = 5
        otp_type_setting_obj.max_attempt_count = 5
        otp_type_setting_obj.save()
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_counter_based').max_attempt_count, 5)
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_counter_based').expire_after, 5)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'general_verification')

        for i in range(OTPTypeSetting.objects.get(otp_type='counter_based').max_attempt_count):
            if i in [0, 1]:
                result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
                self.assertEqual(result, False)
                self.assertEqual(msg, 'wrong_opt_code')
            else:
                time.sleep(5)
                result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
                self.assertEqual(result, False)
                self.assertEqual(msg, 'expired')


    def test_timer_counter_based_check_otp_3(self):
        OTPTypeSetting.objects.delete_invalid_records()
        OTPTypeSetting.objects.create_otp_types()
        otp_type_setting_obj = OTPTypeSetting.objects.get(otp_type='timer_counter_based')
        otp_type_setting_obj.expire_after = 5
        otp_type_setting_obj.max_attempt_count = 5
        otp_type_setting_obj.save()
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_counter_based').max_attempt_count, 5)
        self.assertEqual(OTPTypeSetting.objects.get(otp_type='timer_counter_based').expire_after, 5)
        otp_code, otp_object = OTPCode.objects.create_otp(OTPTypeSetting.objects.get(otp_type='timer_counter_based'), 'general_verification')

        for i in range(OTPTypeSetting.objects.get(otp_type='counter_based').max_attempt_count-1):
            if i == 0:
                result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
                self.assertEqual(result, False)
                self.assertEqual(msg, 'wrong_opt_code')
            elif i == 1:
                time.sleep(2)
                result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
                self.assertEqual(result, False)
                self.assertEqual(msg, 'wrong_opt_code')
            else:
                result, msg, desc = otp_object.check_otp('invalid_input_1234567890', 'general_verification')
                self.assertEqual(result, False)
                self.assertEqual(msg, 'wrong_opt_code')


            result, msg, desc = otp_object.check_otp(otp_code, 'general_verification')
            self.assertEqual(result, True)
            self.assertEqual(msg, None)
