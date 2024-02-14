from django.conf import settings
from django.test import TestCase
from .utils.base_OTP_config_manager import BaseOTPConfigManager
from .utils.base_OTP_config_manager import BaseOTPConfigManager
from .utils.base_OTP_manager import BaseOTPManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import OTPCode
from django.db.models import Q
# Create your tests here.


class BaseOTPConfigManagerTestClass(TestCase):
    maxDiff = None

    def setUp(self):
        # Setup run before every test method.
        pass



    def tearDown(self):
        # Clean up run after every test method.
        pass


# RUN EACH ONE OF THESE TESTS SEPERATELY.
    # def test_config_creation_1(self):
    #     config = None
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     base_OTP_config_manager_object._create_config(config)
    #     expected_config_profiles = {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 5,
    #             'expire_after': 60,
    #             'OTP_length': base_OTP_config_manager_object.default_OTP_length
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 5,
    #             'OTP_length': base_OTP_config_manager_object.default_OTP_length
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': 60,
    #             'OTP_length': base_OTP_config_manager_object.default_OTP_length
    #         }
    #     }
    #     self.assertEqual(base_OTP_config_manager_object.default_OTP_length, 8)
    #     self.assertEqual(base_OTP_config_manager_object.default_max_possible_try, 5)
    #     self.assertEqual(base_OTP_config_manager_object.default_expire_after, 60)
    #     self.assertDictEqual(base_OTP_config_manager_object.config_profiles, expected_config_profiles)
    #     self.assertListEqual(list(base_OTP_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    # def test_config_creation_2(self):
    #     config = {
    #         'default_OTP_length': 19, 
    #         'default_max_possible_try': 81,
    #         'default_expire_after': 37,
    #     }
    #     base_otp_config_manager_object = BaseOTPConfigManager()
    #     base_otp_config_manager_object._create_config(config)
    #     expected_config_profiles = {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
    #             'expire_after': base_otp_config_manager_object.default_expire_after,
    #             'OTP_length': base_otp_config_manager_object.default_OTP_length
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
    #             'OTP_length': base_otp_config_manager_object.default_OTP_length
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': base_otp_config_manager_object.default_expire_after,
    #             'OTP_length': base_otp_config_manager_object.default_OTP_length
    #         }
    #     }
    #     self.assertEqual(base_otp_config_manager_object.default_OTP_length, 19)
    #     self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 81)
    #     self.assertEqual(base_otp_config_manager_object.default_expire_after, 37)
    #     self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
    #     self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    # def test_config_creation_3(self):
    #     config = {
    #         'config_profiles':{
    #             'test_account_verification':{
    #                 'OTP_type': 'timer_counter_based',
    #                 'OTP_usage': 'Account Verification',
    #             },
    #             'test_new_phone_number_verification': {
    #                 'OTP_type': 'counter_based',
    #                 'OTP_usage': 'New Phone Number Verification',
    #                 'max_possible_try': 39,
    #             },
    #             'test_reset_password': {
    #                 'OTP_type': 'timer_based',
    #                 'OTP_usage': 'Forgotten Password',
    #                 'OTP_length': 13
    #             }
    #         }
    #     }
    #     base_otp_config_manager_object = BaseOTPConfigManager()
    #     base_otp_config_manager_object._create_config(config)
    #     expected_config_profiles = {
    #         'test_account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
    #             'expire_after': base_otp_config_manager_object.default_expire_after,
    #             'OTP_length': base_otp_config_manager_object.default_OTP_length
    #         },
    #         'test_new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 39,
    #             'OTP_length': base_otp_config_manager_object.default_OTP_length
    #         },
    #         'test_reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': base_otp_config_manager_object.default_expire_after,
    #             'OTP_length': 13
    #         }
    #     }
    #     self.assertEqual(base_otp_config_manager_object.default_OTP_length, 8)
    #     self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 5)
    #     self.assertEqual(base_otp_config_manager_object.default_expire_after, 60)
    #     self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
    #     self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    # def test_config_creation_4(self):
    #     config = {
    #         'default_OTP_length': 11, 
    #         'default_max_possible_try': 22,
    #         'default_expire_after': 33,
    #         'config_profiles':{
    #             'test_account_verification':{
    #                 'OTP_type': 'timer_counter_based',
    #                 'OTP_usage': 'Account Verification',
    #             },
    #             'test_reset_password': {
    #                 'OTP_type': 'timer_based',
    #                 'OTP_usage': 'Forgotten Password',
    #                 'OTP_length': 13
    #             }
    #         }
    #     }
    #     base_otp_config_manager_object = BaseOTPConfigManager()
    #     base_otp_config_manager_object._create_config(config)
    #     expected_config_profiles = {
    #         'test_account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': base_otp_config_manager_object.default_max_possible_try,
    #             'expire_after': base_otp_config_manager_object.default_expire_after,
    #             'OTP_length': base_otp_config_manager_object.default_OTP_length
    #         },
    #         'test_reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': base_otp_config_manager_object.default_expire_after,
    #             'OTP_length': 13
    #         }
    #     }
    #     self.assertEqual(base_otp_config_manager_object.default_OTP_length, 11)
    #     self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 22)
    #     self.assertEqual(base_otp_config_manager_object.default_expire_after, 33)
    #     self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
    #     self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    # def test_config_creation_5(self):
    #         # Add OTP_MODULE_CONFIG in your settings and copy the following config
    #             # OTP_MODULE_CONFIG = {
    #             #         'default_OTP_length': 14, 
    #             #         'default_max_possible_try': 1,
    #             #         'default_expire_after': 369,
    #             #         'config_profiles': {
    #             #         'test_account_verification':{
    #             #             'OTP_type': 'timer_counter_based',
    #             #             'OTP_usage': 'Account Verification',
    #             #         },
    #             #         'test_new_phone_number_verification': {
    #             #             'OTP_type': 'counter_based',
    #             #             'OTP_usage': 'New Phone Number Verification',
    #             #             'max_possible_try': 3,
    #             #             'OTP_length': 6
    #             #         },
    #             #         'test_reset_password': {
    #             #             'OTP_type': 'timer_based',
    #             #             'OTP_usage': 'Forgotten Password',
    #             #             'expire_after': 120
    #             #         }
    #             #     }
    #             # }
    #         config = None
    #         base_otp_config_manager_object = BaseOTPConfigManager()
    #         base_otp_config_manager_object._create_config(config)
    #         expected_config_profiles = {
    #             'test_account_verification':{
    #                 'OTP_type': 'timer_counter_based',
    #                 'OTP_usage': 'Account Verification',
    #                 'max_possible_try': 1,
    #                 'expire_after': 369,
    #                 'OTP_length': 14
    #             },
    #             'test_new_phone_number_verification': {
    #                 'OTP_type': 'counter_based',
    #                 'OTP_usage': 'New Phone Number Verification',
    #                 'max_possible_try': 3,
    #                 'OTP_length': 6
    #             },
    #             'test_reset_password': {
    #                 'OTP_type': 'timer_based',
    #                 'OTP_usage': 'Forgotten Password',
    #                 'expire_after': 120,
    #                 'OTP_length': 14
    #             }
    #         }
    #         self.assertEqual(base_otp_config_manager_object.default_OTP_length, 14)
    #         self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 1)
    #         self.assertEqual(base_otp_config_manager_object.default_expire_after, 369)
    #         self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
    #         self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    # def test_config_creation_6(self):
    #     # add OTP_MODULE_CONFIG in your settings and copy the following config
    #         # OTP_MODULE_CONFIG = {
    #         #         'config_profiles': {
    #         #         'test_account_verification':{
    #         #             'OTP_type': 'timer_counter_based',
    #         #             'OTP_usage': 'Account Verification',
    #         #         },
    #         #         'test_new_phone_number_verification': {
    #         #             'OTP_type': 'counter_based',
    #         #             'OTP_usage': 'New Phone Number Verification',
    #         #             'max_possible_try': 3,
    #         #             'OTP_length': 6
    #         #         },
    #         #         'test_reset_password': {
    #         #             'OTP_type': 'timer_based',
    #         #             'OTP_usage': 'Forgotten Password',
    #         #             'expire_after': 120
    #         #         }
    #         #     }
    #         # }
    #     config = {
    #         'default_OTP_length': 19, 
    #         'default_max_possible_try': 81,
    #         'default_expire_after': 37,
    #     }
    #     base_otp_config_manager_object = BaseOTPConfigManager()
    #     base_otp_config_manager_object._create_config(config)
    #     expected_config_profiles = {
    #         'test_account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 81,
    #             'expire_after': 37,
    #             'OTP_length': 19
    #         },
    #         'test_new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 3,
    #             'OTP_length': 6
    #         },
    #         'test_reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': 120,
    #             'OTP_length': 19
    #         }
    #     }
    #     self.assertEqual(base_otp_config_manager_object.default_OTP_length, 19)
    #     self.assertEqual(base_otp_config_manager_object.default_max_possible_try, 81)
    #     self.assertEqual(base_otp_config_manager_object.default_expire_after, 37)
    #     self.assertDictEqual(base_otp_config_manager_object.config_profiles, expected_config_profiles)
    #     self.assertListEqual(list(base_otp_config_manager_object.config_profiles.keys()), list(expected_config_profiles.keys()))



    # def test_config_creation_7(self):
    #     # add OTP_MODULE_CONFIG in your settings and copy the following config
    #         # OTP_MODULE_CONFIG = {
    #         #     'default_OTP_length': 19, 
    #         #     'default_max_possible_try': 81,
    #         #     'default_expire_after': 37,
    #         # }
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #         },
    #         'new_phone_number_verification2': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification2',
    #             'max_possible_try': 9,
    #             'newItem': 12
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #         },
    #         'reset_password2': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password2',
    #             'expire_after': 300,
    #             'max_possible_try': 12,
    #             'anotherThing': None
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)

    #     expected_config_profiles = {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 81,
    #             'expire_after': 37,
    #             'OTP_length': 19
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 81,
    #             'OTP_length': 19

    #         },
    #         'new_phone_number_verification2': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification2',
    #             'max_possible_try': 9,
    #             'OTP_length': 19

    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': 37,
    #             'OTP_length': 19

    #         },
    #         'reset_password2': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password2',
    #             'expire_after': 300,
    #             'OTP_length': 19

    #         }
    #     }

    #     self.assertEqual(base_OTP_config_manager_object.default_OTP_length, 19)
    #     self.assertEqual(base_OTP_config_manager_object.default_max_possible_try, 81)
    #     self.assertEqual(base_OTP_config_manager_object.default_expire_after, 37)
    #     self.assertDictEqual(base_OTP_config_manager_object.config_profiles, expected_config_profiles)




    # def test_config_creation_7_reverse(self):
    #     # add OTP_MODULE_CONFIG in your settings and copy the following config
    #         # OTP_MODULE_CONFIG = {
    #         #     'config_profiles': {
    #         #     'account_verification':{
    #         #         'OTP_type': 'timer_counter_based',
    #         #         'OTP_usage': 'Account Verification',
    #         #     },
    #         #     'new_phone_number_verification': {
    #         #         'OTP_type': 'counter_based',
    #         #         'OTP_usage': 'New Phone Number Verification',
    #         #     },
    #         #     'new_phone_number_verification2': {
    #         #         'OTP_type': 'counter_based',
    #         #         'OTP_usage': 'New Phone Number Verification2',
    #         #         'max_possible_try': 9,
    #         #         'newItem': 12
    #         #     },
    #         #     'reset_password': {
    #         #         'OTP_type': 'timer_based',
    #         #         'OTP_usage': 'Forgotten Password',
    #         #     },
    #         #     'reset_password2': {
    #         #         'OTP_type': 'timer_based',
    #         #         'OTP_usage': 'Forgotten Password2',
    #         #         'expire_after': 300,
    #         #         'max_possible_try': 12,
    #         #         'anotherThing': None
    #         #     }
    #         #     }
    #         # }
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 19, 
    #         'default_max_possible_try': 81,
    #         'default_expire_after': 37,
    #     }

    #     base_OTP_config_manager_object._create_config(config)

    #     expected_config_profiles = {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 81,
    #             'expire_after': 37,
    #             'OTP_length': 19
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 81,
    #             'OTP_length': 19

    #         },
    #         'new_phone_number_verification2': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification2',
    #             'max_possible_try': 9,
    #             'OTP_length': 19

    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': 37,
    #             'OTP_length': 19

    #         },
    #         'reset_password2': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password2',
    #             'expire_after': 300,
    #             'OTP_length': 19

    #         }
    #     }

    #     self.assertEqual(base_OTP_config_manager_object.default_OTP_length, 19)
    #     self.assertEqual(base_OTP_config_manager_object.default_max_possible_try, 81)
    #     self.assertEqual(base_OTP_config_manager_object.default_expire_after, 37)
    #     self.assertDictEqual(base_OTP_config_manager_object.config_profiles, expected_config_profiles)



    # def test_config_creation_8(self):
    #     # Checking if an unwanted key in config (but not in config_profiles) can break the app or not
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12,
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'anotherThing': "Something",
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #         },
    #         'new_phone_number_verification2': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification2',
    #             'max_possible_try': 9,
    #             'newItem': 12
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #         },
    #         'reset_password2': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password2',
    #             'expire_after': 300,
    #             'max_possible_try': 12,
    #             'anotherThing': None
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)

    #     expected_config_profiles = {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 12,
    #             'expire_after': 600,
    #             'OTP_length': 12
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 12,
    #             'OTP_length': 12
    #         },
    #         'new_phone_number_verification2': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification2',
    #             'max_possible_try': 9,
    #             'OTP_length': 12
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'expire_after': 600,
    #             'OTP_length': 12
    #         },
    #         'reset_password2': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password2',
    #             'expire_after': 300,
    #             'OTP_length': 12
    #         }
    #     }

    #     self.assertEqual(base_OTP_config_manager_object.default_OTP_length, 12)
    #     self.assertEqual(base_OTP_config_manager_object.default_max_possible_try, 12)
    #     self.assertEqual(base_OTP_config_manager_object.default_expire_after, 600)
    #     self.assertDictEqual(base_OTP_config_manager_object.config_profiles, expected_config_profiles)



    # def test_config_creation_9(self):
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     expected_config_profiles = {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'OTP_length': 12,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'OTP_length': 12,
    #             'max_possible_try': 8
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'OTP_length': 12,
    #             'expire_after': 90
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertEqual(base_OTP_config_manager_object.default_OTP_length, 12)
    #     self.assertEqual(base_OTP_config_manager_object.default_max_possible_try, 12)
    #     self.assertEqual(base_OTP_config_manager_object.default_expire_after, 600)
    #     self.assertDictEqual(base_OTP_config_manager_object.config_profiles, expected_config_profiles)



    # def test_config_creation_10(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when two same keys exist in config.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'default_expire_after': 200,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(KeyError)



    # def test_config_creation_11(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when two same keys exist in config.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {

    #         },
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(KeyError)



    # def test_config_creation_12(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when two same keys exist in config.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification2',
    #             'max_possible_try': 8,
    #             'expire_after': 180
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(KeyError)



    # def test_config_creation_13(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when two same keys exist in config.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 120,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(KeyError)



    # def test_config_creation_14(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when config contains invalid OTP_type.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_bas',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 120,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(ValueError)



    # def test_config_creation_15(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when passing anything except dict to config_profiles.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': 'notADict'
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(ValueError)



    # def test_config_creation_16(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when passing anything except dict to one of config_profiles profiles.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification': 'notADict',
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_bas',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 120,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(ValueError)



    # def test_config_creation_17(self):
    #     # Checking that BaseOTPConfigManagerObject raise proper error when passing anything except dict to one of config_profiles profiles.
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     base_OTP_config_manager_object.defaultConfig = None
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification': 'notADict',
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_bas',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 120,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     base_OTP_config_manager_object._create_config(config)
    #     self.assertRaises(ValueError)



    # def test_retirieving_config_based_on_OTP_usage_1(self):
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }
    #     expected_config_profiles = {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'OTP_length': 12
    #         }
    #     base_OTP_config_manager_object._create_config(config)
    #     retirievedConfig = base_OTP_config_manager_object._get_config_based_on_OTP_config_profile_name('new_phone_number_verification')
    #     self.assertEqual(retirievedConfig, expected_config_profiles)



    # def test_retirieving_config_based_on_OTP_usage_2(self):
    #     base_OTP_config_manager_object = BaseOTPConfigManager()
    #     config = {
    #         'default_OTP_length': 12, 
    #         'default_max_possible_try': 12,
    #         'default_expire_after': 600,
    #         'config_profiles': {
    #         'account_verification':{
    #             'OTP_type': 'timer_counter_based',
    #             'OTP_usage': 'Account Verification',
    #             'max_possible_try': 7,
    #             'expire_after': 120
    #         },
    #         'new_phone_number_verification': {
    #             'OTP_type': 'counter_based',
    #             'OTP_usage': 'New Phone Number Verification',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         },
    #         'reset_password': {
    #             'OTP_type': 'timer_based',
    #             'OTP_usage': 'Forgotten Password',
    #             'max_possible_try': 8,
    #             'expire_after': 90
    #         }
    #         }
    #     }

    #     base_OTP_config_manager_object._create_config(config)
    #     base_OTP_config_manager_object._get_config_based_on_OTP_config_profile_name('Dummy_Name')
    #     self.assertRaises(Exception)





# DO NOT CAHNGE CONFIG FOR GENERATING OTP CODES.
class BaseOTPConfigManagerTestClass(TestCase):
    def test_timer_counter_based_OTP_1(self):
        # Checking timer_counter_based OTP generation and successful validation.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = False,
            is_active = False,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'account_verification')
        otp = OTP_code_object.otp
        self.assertEqual(OTP_code_object.user, user)
        self.assertEqual(len(OTP_code_object.otp), base_OTP_manager.default_OTP_length)
        self.assertEqual(OTP_code_object.otp.isdigit(), True)
        self.assertEqual(OTP_code_object.otp_type, base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_type"])
        self.assertEqual(OTP_code_object.otp_usage, base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_usage"])
        self.assertEqual(OTP_code_object.expire_after, base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["expire_after"])
        self.assertEqual(OTP_code_object.try_counter, 0)
        self.assertEqual(OTP_code_object.max_possible_try, base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["max_possible_try"])
        self.assertNotEqual(OTP_code_object.last_try, None)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_usage"]))), 1)
        response = base_OTP_manager.verify_OTP(user, 'account_verification', str(int(otp)+15))
        self.assertDictEqual(response.data, {'OTP': "OTP code Is Wrong."})
        self.assertEqual(response.status_code, 403)
        OTP_code_object = OTPCode.objects.get(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_usage"]))
        self.assertEqual(OTP_code_object.try_counter, 1)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_usage"]))), 1)
        response = base_OTP_manager.verify_OTP(user, 'account_verification', otp)
        self.assertDictEqual(response.data, {'OTP': "OTP Is Correct."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_usage"]))), 0)
        response = base_OTP_manager.verify_OTP(user, 'account_verification', otp)
        self.assertDictEqual(response.data, {'OTP': "No OTP Exists. Request OTP again."})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')["OTP_usage"]))), 0)
        user.delete()



    def test_timer_counter_based_OTP_2(self):
        # Checking timer_counter_based OTP unsuccessful validation responses -- expired OTP.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = False,
            is_active = False,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'account_verification')

        # Expiring OTP.
        OTP_code_object.expire_after = 0
        OTP_code_object.save()
        response = base_OTP_manager.verify_OTP(user, 'account_verification', OTP_code_object.otp)
        self.assertDictEqual(response.data, {'OTP': "OTP Is Expired."})
        self.assertEqual(response.status_code, 403)



    def test_timer_counter_based_OTP_3(self):
        # Checking timer_counter_based OTP unsuccessful validation responses -- too many tries.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = False,
            is_active = False,
            new_phone_number = None,
            is_new_phone_verified = True,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'account_verification')

        # Changing counter number.
        OTP_code_object.try_counter = base_OTP_manager.get_config_based_on_OTP_config_profile_name('account_verification')['max_possible_try']
        OTP_code_object.save()
        response = base_OTP_manager.verify_OTP(user, 'account_verification', OTP_code_object.otp)
        self.assertDictEqual(response.data, {'OTP': "Too Many Tries. Request OTP again."})
        self.assertEqual(response.status_code, 403)




    def test_counter_based_OTP_1(self):
        # Checking counter_based OTP.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = '09365451122',
            is_new_phone_verified = False,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'new_phone_number_verification')
        otp = OTP_code_object.otp
        self.assertEqual(OTP_code_object.user, user)
        self.assertEqual(OTP_code_object.otp.isdigit(), True)
        self.assertEqual(len(OTP_code_object.otp), base_OTP_manager.default_OTP_length)
        self.assertEqual(OTP_code_object.otp_type, base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_type"])
        self.assertEqual(OTP_code_object.otp_usage, base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_usage"])
        self.assertEqual(OTP_code_object.try_counter, 0)
        self.assertEqual(OTP_code_object.max_possible_try, base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["max_possible_try"])
        self.assertNotEqual(OTP_code_object.last_try, None)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_usage"]))), 1)
        response = base_OTP_manager.verify_OTP(user, 'new_phone_number_verification', str(int(otp)-100))
        self.assertDictEqual(response.data, {'OTP': "OTP code Is Wrong."})
        self.assertEqual(response.status_code, 403)
        OTP_code_object = OTPCode.objects.get(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_usage"]))
        self.assertEqual(OTP_code_object.try_counter, 1)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_usage"]))), 1)
        response = base_OTP_manager.verify_OTP(user, 'new_phone_number_verification', otp)
        self.assertDictEqual(response.data, {'OTP': "OTP Is Correct."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_usage"]))), 0)
        response = base_OTP_manager.verify_OTP(user, 'new_phone_number_verification', otp)
        self.assertDictEqual(response.data, {'OTP': "No OTP Exists. Request OTP again."})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')["OTP_usage"]))), 0)
        user.delete()



    def test_counter_based_OTP_2(self):
        # # Checking counter_based OTP.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = '09365451122',
            is_new_phone_verified = False,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'new_phone_number_verification')

        # Changing counter number.
        OTP_code_object.try_counter = base_OTP_manager.get_config_based_on_OTP_config_profile_name('new_phone_number_verification')['max_possible_try']
        OTP_code_object.save()
        response = base_OTP_manager.verify_OTP(user, 'new_phone_number_verification', OTP_code_object.otp)
        self.assertDictEqual(response.data, {'OTP': "Too Many Tries. Request OTP again."})
        self.assertEqual(response.status_code, 403)





    def test_timer_based_OTP_1(self):
        # # Checking counter_based OTP.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = '09365451122',
            is_new_phone_verified = False,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'reset_password')
        otp = OTP_code_object.otp
        self.assertEqual(OTP_code_object.user, user)
        self.assertEqual(OTP_code_object.otp.isdigit(), True)
        self.assertEqual(len(OTP_code_object.otp), base_OTP_manager.default_OTP_length)
        self.assertEqual(OTP_code_object.otp_type, base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_type"])
        self.assertEqual(OTP_code_object.otp_usage, base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_usage"])
        self.assertEqual(OTP_code_object.try_counter, 0)
        self.assertNotEqual(OTP_code_object.expire_after, None)
        self.assertNotEqual(OTP_code_object.last_try, None)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_usage"]))), 1)
        response = base_OTP_manager.verify_OTP(user, 'reset_password', str(int(otp)-100))
        self.assertDictEqual(response.data, {'OTP': "OTP code Is Wrong."})
        self.assertEqual(response.status_code, 403)
        OTP_code_object = OTPCode.objects.get(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_usage"]))
        self.assertNotEqual(OTP_code_object.last_try, None)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_usage"]))), 1)
        response = base_OTP_manager.verify_OTP(user, 'reset_password', otp)
        self.assertDictEqual(response.data, {'OTP': "OTP Is Correct."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_usage"]))), 0)
        response = base_OTP_manager.verify_OTP(user, 'reset_password', otp)
        self.assertDictEqual(response.data, {'OTP': "No OTP Exists. Request OTP again."})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(OTPCode.objects.filter(Q(user=user) & Q(otp_usage=base_OTP_manager.get_config_based_on_OTP_config_profile_name('reset_password')["OTP_usage"]))), 0)
        user.delete()



    def test_timer_based_OTP_1(self):
        # # Checking counter_based OTP.
        UserModel = get_user_model()
        user = UserModel.objects.create(
            first_name = 'test first_name',
            last_name = 'test last_name',
            phone_number = '09361234567',
            email = 'testuser@mail.com',
            is_account_verified = True,
            is_active = True,
            new_phone_number = '09365451122',
            is_new_phone_verified = False,
            password = make_password('test_user_12345')
        )
        base_OTP_manager = BaseOTPManager()
        OTP_code_object = base_OTP_manager.generate_OTP(user, 'reset_password')

        # Expiring OTP.
        OTP_code_object.expire_after = 0
        OTP_code_object.save()
        response = base_OTP_manager.verify_OTP(user, 'reset_password', OTP_code_object.otp)
        self.assertDictEqual(response.data, {'OTP': "OTP Is Expired."})
        self.assertEqual(response.status_code, 403)