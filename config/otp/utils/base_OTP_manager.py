from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from otp.models import OTPCode
from random import randint
from .base_OTP_config_manager import BaseOTPConfigManager


UserModel = get_user_model()



class BaseOTPManager(BaseOTPConfigManager):

    OTP_code_object = None
    config = {
            'default_OTP_length': 8, 
            'default_max_possible_try': 5,
            'default_expire_after': 60,
            'config_profiles': {
            'account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
                'max_possible_try': 5,
                'expire_after': 60
            },
            'new_phone_number_verification': {
                'OTP_type': 'counter_based',
                'OTP_usage': 'New Phone Number Verification',
                'max_possible_try': 5,
                'expire_after': 60
            },
            'reset_password': {
                'OTP_type': 'timer_based',
                'OTP_usage': 'Forgotten Password',
                'max_possible_try': 5,
                'expire_after': 60
            }
            }
        }

    def get_config(self):
        self._create_config(self.config)



    def after_OTP_verification_action(self, user):
        return self.successful_validation_message()


    def no_OTP_exists(self):
        return Response(data={'OTP': "No OTP Exists. Request OTP again."}, status=status.HTTP_404_NOT_FOUND)


    def too_many_tries(self):
        return Response(data={'OTP': "Too Many Tries. Request OTP again."}, status=status.HTTP_403_FORBIDDEN)


    def wrong_OTP_input(self):
        return Response(data={'OTP': "OTP code Is Wrong."}, status=status.HTTP_403_FORBIDDEN)


    def OTP_expired(self):
        return Response(data={'OTP': "OTP Is Expired."}, status=status.HTTP_403_FORBIDDEN)
    
    def successful_validation_message(self):
        return Response(data={'OTP': "OTP Is Correct."}, status=status.HTTP_200_OK)


    def create_random_digits(self, char_count):
        # allowedChars = string.digits
        # return int(''.join(random.choices(allowedChars, k=char_count)))
        range_start = 10**(char_count-1)
        range_start = (10**char_count)-1
        return str(randint(range_start, range_start))



    def OTP_query(self, user, OTP_type, OTP_usage):
        # In case you have more than one object of a specific otp for any reason.
        OTP_code_objects = OTPCode.objects.filter(Q(user = user) & Q(otp_type = OTP_type) & Q(otp_usage = OTP_usage))
        if len(OTP_code_objects) > 1:
            is_first_round = True
            for i in range(len(OTP_code_objects)):
                if is_first_round == True:
                    latest_creation_date = OTP_code_objects[i].otp_creation_date
                    self.OTP_code_object = OTP_code_objects[i]
                    is_first_round = False
                    continue
                if latest_creation_date < OTP_code_objects[i].otp_creation_date:
                    latest_creation_date = OTP_code_objects[i].otp_creation_date
                    self.OTP_code_object = OTP_code_objects[i]

            for i in range(len(OTP_code_objects)):
                if self.OTP_code_object.pk != OTP_code_objects[i].pk:
                    OTP_code_objects[i].delete()
        elif len(OTP_code_objects) == 1:
            self.OTP_code_object = OTP_code_objects[0]
        else:
            self.OTP_code_object = None




    def generate_OTP(self, user, OTP_config_name):
        config = self.get_config_based_on_OTP_config_profile_name(OTP_config_name)
        self.OTP_query(user, config['OTP_type'], config['OTP_usage'])

        if config['OTP_type'] == "timer_counter_based":
            return self.generate_timer_and_counter_based_OTP(self.OTP_code_object, user, config['OTP_type'], config['OTP_usage'], config['OTP_length'], config['max_possible_try'], config['expire_after'])
        elif config['OTP_type'] == "counter_based":
            return self.generate_counter_based_OTP(self.OTP_code_object, user, config['OTP_type'], config['OTP_usage'], config['OTP_length'], config['max_possible_try'])
        elif config['OTP_type'] == "timer_based":
            return self.generate_timer_based_OTP(self.OTP_code_object, user, config['OTP_type'], config['OTP_usage'], config['OTP_length'], config['expire_after'])



    def generate_timer_and_counter_based_OTP(self, OTP_code_object, user, OTP_type, OTP_usage, OTP_length, max_possible_try, expire_after):
        if OTP_code_object is None:
            OTP_code_object = OTPCode.objects.create(user = user, 
                                                   otp = self.create_random_digits(OTP_length),
                                                   otp_type = OTP_type, 
                                                   otp_usage = OTP_usage, 
                                                   max_possible_try = max_possible_try,
                                                    expire_after = expire_after)
        else:
            OTP_code_object.otp = self.create_random_digits(OTP_length)
            OTP_code_object.otp_usage = OTP_usage
            OTP_code_object.max_possible_try = max_possible_try
            OTP_code_object.expire_after = expire_after
            OTP_code_object.last_try = None
            OTP_code_object.otp_creation_date = timezone.now()
            OTP_code_object.save()
        return OTP_code_object

    

    def generate_counter_based_OTP(self, OTP_code_object, user, OTP_type, OTP_usage, OTP_length, max_possible_try):
        if OTP_code_object is None:
            OTP_code_object = OTPCode.objects.create(user = user, 
                                                   otp = self.create_random_digits(OTP_length),
                                                   otp_type = OTP_type, 
                                                   otp_usage = OTP_usage, 
                                                   max_possible_try = max_possible_try)
        else:
            OTP_code_object.otp = self.create_random_digits(OTP_length)
            OTP_code_object.otp_usage = OTP_usage
            OTP_code_object.max_possible_try = max_possible_try
            OTP_code_object.last_try = None
            OTP_code_object.otp_creation_date = timezone.now()
            OTP_code_object.save()
        return OTP_code_object



    def generate_timer_based_OTP(self, OTP_code_object, user, OTP_type, OTP_usage, OTP_length, expire_after):
        if OTP_code_object is None:
            OTP_code_object = OTPCode.objects.create(user = user, 
                                                   otp = self.create_random_digits(OTP_length),
                                                   otp_type = OTP_type, 
                                                   otp_usage = OTP_usage,
                                                   expire_after = expire_after)
        else:
            OTP_code_object.otp = self.create_random_digits(OTP_length)
            OTP_code_object.otp_usage = OTP_usage
            OTP_code_object.expire_after = expire_after
            OTP_code_object.last_try = None
            OTP_code_object.otp_creation_date = timezone.now()
            OTP_code_object.save()
        return OTP_code_object



    def verify_OTP(self, user, OTP_config_name, user_input_code):
        """
        If verification is successful, it automatically calls after_OTP_verification_action
        and passes related object to it.
        """
        config = self.get_config_based_on_OTP_config_profile_name(OTP_config_name)
        self.OTP_query(user, config['OTP_type'], config['OTP_usage'])

        if self.OTP_code_object == None:
            return self.no_OTP_exists()

        if config['OTP_type'] == "timer_counter_based":
            return self.verify_timer_and_counter_based_OTP(user, user_input_code)
        elif config['OTP_type'] == "counter_based":
            return self.verify_counter_based_OTP(user, user_input_code)
        elif config['OTP_type'] == "timer_based":
            return self.verify_timer_based_OTP(user, user_input_code)



    def verify_timer_and_counter_based_OTP(self, user, user_input_code):
        if self.OTP_code_object.has_time() == True:
            if self.OTP_code_object.can_try() == True:
                if self.OTP_code_object.otp == user_input_code:
                    self.OTP_code_object.delete()
                    return self.after_OTP_verification_action(user)
                else:
                    self.OTP_code_object.increment_try_counter_value()
                    return self.wrong_OTP_input()
            else:
                return self.too_many_tries()
        else:
            return self.OTP_expired()



    def verify_counter_based_OTP(self, user, user_input_code):
        if self.OTP_code_object.can_try() == True:
            if self.OTP_code_object.otp == user_input_code:
                self.OTP_code_object.delete()
                return self.after_OTP_verification_action(user)
            else:
                self.OTP_code_object.increment_try_counter_value()
                return self.wrong_OTP_input()
        else:
            return self.too_many_tries()
        


    def verify_timer_based_OTP(self, user, user_input_code):
        if self.OTP_code_object.has_time() == True:
            if self.OTP_code_object.otp == user_input_code:
                self.OTP_code_object.delete()
                return  self.after_OTP_verification_action(user)
            else:
                # self.OTP_code_object.increment_try_counter_value()
                return self.wrong_OTP_input()
        else:
            return self.OTP_expired()
        


    def get_config_based_on_OTP_config_profile_name(self, OTP_config_name):
        self.get_config()
        return self._get_config_based_on_OTP_config_profile_name(OTP_config_name)



    def get_OTP_model_object_by_user_input_code(self, user_input_code, OTP_config_name=None):
        try:
            config = self.get_config_based_on_OTP_config_profile_name(OTP_config_name)
            return OTPCode.objects.get(Q(otp_usage=config['OTP_usage']) & Q(otp=user_input_code))
        except OTPCode.DoesNotExist:
            return None
        # config = self.get_config_based_on_OTP_config_profile_name(OTP_config_name)
        # OTP_code_object = OTPCode.objects.filter(Q(otp_usage=config['OTP_usage']) & Q(otp=user_input_code))
        # if len(OTP_code_object) > 0:
        #     return OTP_code_object[0]
        # return None
        

    def get_OTP_model_object_by_user_id(self, user_id, OTP_config_name=None):
        try:
            config = self.get_config_based_on_OTP_config_profile_name(OTP_config_name)
            return OTPCode.objects.get(Q(otp_usage=config['OTP_usage']) & Q(pk=user_id))
        except OTPCode.DoesNotExist:
            return None
        # config = self.get_config_based_on_OTP_config_profile_name(OTP_config_name)
        # OTP_code_object = OTPCode.objects.filter(Q(otp_usage=config['OTP_usage']) & Q(pk=user_id))
        # if len(OTP_code_object) > 0:
        #     return OTP_code_object[0]
        # return None