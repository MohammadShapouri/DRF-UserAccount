from .acceptable_OTP_values import least_acceptable_OTP_length, most_acceptable_OTP_length, least_acceptable_expire_after_time, least_acceptable_max_possible_try
from django.conf import settings



class BaseOTPConfigManager:
    """
    By passing `OTP_length`, `max_possible_try` and `expire_after` in config_profiles, you can customize them.
    """
    default_OTP_length = None
    default_max_possible_try = None
    default_expire_after = None
    config_profiles = dict()

    default_config = {
            'default_OTP_length': 8, 
            'default_max_possible_try': 5,
            'default_expire_after': 60,
            'config_profiles': {
            'account_verification':{
                'OTP_type': 'timer_counter_based',
                'OTP_usage': 'Account Verification',
            },
            'new_phone_number_verification': {
                'OTP_type': 'counter_based',
                'OTP_usage': 'New Phone Number Verification',
            },
            'reset_password': {
                'OTP_type': 'timer_based',
                'OTP_usage': 'Forgotten Password',
            }
        }
    }



    def _create_config(self, config):
        # Validates default_config.
        if type(self.default_config) != dict:
            raise ValueError('Initial config type must be dictionary.')
        else:
            self.validate_config_keys(list(self.default_config.keys()))

        if config == None:
            config = dict()
        else:
            self.validate_config_keys(list(config.keys()))

        if self.default_OTP_length == None:
            self.default_OTP_length = self.get_numeric_variable('default_OTP_length', config.get('default_OTP_length'))
        if self.default_max_possible_try == None:
            self.default_max_possible_try = self.get_numeric_variable('default_max_possible_try', config.get('default_max_possible_try'))
        if self.default_expire_after == None:
            self.default_expire_after = self.get_numeric_variable('default_expire_after', config.get('default_expire_after'))
        if len(self.config_profiles.keys()) == 0:
            self.config_profiles = self.parse_config_profile(config.get('config_profiles'))


    def parse_config_profile(self, config_profiles):
        default_config_profiles = self.default_config.get('config_profiles')
        selected_config_profiles = dict()
        settings_config_profiles = dict()

        try:
            settings_config_profiles = settings.OTP_MODULE_CONFIG
        except AttributeError:
            pass
        settings_config_profiles = settings_config_profiles.get('config_profiles')


        if config_profiles == None and default_config_profiles == None and settings_config_profiles == None:
            raise ValueError('None is not acceptable, Enter a dict as config_profiles or inital config_profiles.')

        if config_profiles != None:
            selected_config_profiles = config_profiles
        else:
            if settings_config_profiles != None:
                selected_config_profiles = settings_config_profiles
            else:
                selected_config_profiles = default_config_profiles

        self.validate_config(selected_config_profiles)

        parsed_dict = dict()

        config_sub_dict_list = list(selected_config_profiles.items())
        for each_config_profile_name, each_config_profile_details in config_sub_dict_list:
            if each_config_profile_details.get('OTP_type') == 'timer_counter_based':
                each_config_parsed_details = self.parse_timer_counter_based_config_detail(each_config_profile_details)
            elif each_config_profile_details.get('OTP_type') == 'counter_based':
                each_config_parsed_details = self.parse_counter_based_config_detail(each_config_profile_details)
            elif each_config_profile_details.get('OTP_type') == 'timer_based':
                each_config_parsed_details = self.parse_timer_based_config_detail(each_config_profile_details)
            parsed_dict[each_config_profile_name] = each_config_parsed_details
        return parsed_dict



    def get_numeric_variable(self, target, variable):
        default = self.default_config.get(target)
        settings_value = None
        try:
            settings_value = settings.OTP_MODULE_CONFIG.get(target)
        except AttributeError:
            pass

        if variable == None and default == None and settings_value == None:
            raise ValueError('None is not acceptable, Enter a number as variable or default or setting variable')

        self.validate_numeric_values(target, variable)
        self.validate_numeric_values(target, settings_value)
        self.validate_numeric_values(target, default)

        if variable != None:
            return int(variable)
        else:
            if settings_value != None:
                return int(settings_value)
        return int(default)



    def validate_numeric_values(self, target, value):
        if value != None:
            value = str(value)
            if str.isdigit(value) == False:
                raise TypeError(f'{target} must be numeric.')
            
            if target == 'OTP_length' or target == 'default_OTP_length':
                value = int(value)
                if value < least_acceptable_OTP_length:
                    raise Exception(f'{target} must contain at least {least_acceptable_OTP_length} characters.')
                if value > most_acceptable_OTP_length:
                    raise Exception(f'{target} must contain at most {most_acceptable_OTP_length} characters.')
            if target == 'max_possible_try' or target == 'default_max_possible_try':
                value = int(value)
                if value < least_acceptable_max_possible_try:
                    raise Exception(f'{target} must be at least {least_acceptable_max_possible_try}.')
            if target == 'expire_after' or target == 'default_expire_after':
                value = int(value)
                if value < least_acceptable_expire_after_time:
                    raise Exception(f'{target} must be at least {least_acceptable_expire_after_time}.')



    def validate_config(self, config_profiles):
        if config_profiles != None:
            if type(config_profiles) != dict:
                raise ValueError('Config profiles type must be dictionary.')
            
            config_profiles_list = list(config_profiles.values())
            config_profiles_keys = list(config_profiles.keys())
            self.validate_config_profiles_keys(config_profiles_keys)
            for each_config_profile_details in config_profiles_list:
                self.validate_each_config_profile_details(each_config_profile_details)



    def validate_config_profiles_keys(self, config_profiles_keys):
        for each_key in config_profiles_keys:
            if config_profiles_keys.count(each_key) > 1:
                raise KeyError('Can\'t use one key multiple times as config profile name.')



    def validate_config_keys(self, config_keys):
        for each_key in config_keys:
            if config_keys.count(each_key) > 1:
                raise KeyError('Can\'t use one key multiple times.')



    def validate_each_config_profile_details(self, each_config_profile_details):
        if each_config_profile_details != None:
            if type(each_config_profile_details) != dict:
                raise ValueError('Config profile type must be dictionary.')
            # each_config_profile_s_keys = each config profile's keys in english.
            each_config_profile_s_keys = list(each_config_profile_details.keys())
            for each_key in each_config_profile_s_keys:
                if each_config_profile_s_keys.count(each_key) > 1:
                    raise KeyError('Can\'t use one key multiple times inside one config profile.')

            valid_OTP_type_inputs = ['timer_counter_based', 'counter_based', 'timer_based']
            if each_config_profile_details.get('OTP_type') not in valid_OTP_type_inputs:
                raise ValueError("OTP_type: OTP_type must be one of %r." % valid_OTP_type_inputs)
            if each_config_profile_details.get('OTP_usage') == None:
                raise ValueError("OTP_usage: OTP_usage must not be empty")
            if each_config_profile_details.get('max_possible_try') != None:
                self.validate_numeric_values('max_possible_try', each_config_profile_details.get('max_possible_try'))
            if each_config_profile_details.get('expire_after') != None:
                self.validate_numeric_values('expire_after', each_config_profile_details.get('expire_after'))
            if each_config_profile_details.get('OTP_length') != None:
                self.validate_numeric_values('OTP_length', each_config_profile_details.get('OTP_length'))



    def parse_timer_counter_based_config_detail(self, each_config_profile_details):
        parsed_config_profile_details = dict()

        parsed_config_profile_details['OTP_type'] = each_config_profile_details.get('OTP_type')
        parsed_config_profile_details['OTP_usage'] = each_config_profile_details.get('OTP_usage')

        if each_config_profile_details.get('max_possible_try') == None:
            parsed_config_profile_details['max_possible_try'] = self.default_max_possible_try
        else:
            parsed_config_profile_details['max_possible_try'] = each_config_profile_details.get('max_possible_try')

        if each_config_profile_details.get('expire_after') == None:
            parsed_config_profile_details['expire_after'] = self.default_expire_after
        else:
            parsed_config_profile_details['expire_after'] = each_config_profile_details.get('expire_after')

        if each_config_profile_details.get('OTP_length') == None:
            parsed_config_profile_details['OTP_length'] = self.default_OTP_length
        else:
            parsed_config_profile_details['OTP_length'] = each_config_profile_details.get('OTP_length')

        return parsed_config_profile_details



    def parse_counter_based_config_detail(self, each_config_profile_details):
        parsed_config_profile_details = dict()

        parsed_config_profile_details['OTP_type'] = each_config_profile_details.get('OTP_type')
        parsed_config_profile_details['OTP_usage'] = each_config_profile_details.get('OTP_usage')

        if each_config_profile_details.get('max_possible_try') == None:
            parsed_config_profile_details['max_possible_try'] = self.default_max_possible_try
        else:
            parsed_config_profile_details['max_possible_try'] = each_config_profile_details.get('max_possible_try')

        if each_config_profile_details.get('OTP_length') == None:
            parsed_config_profile_details['OTP_length'] = self.default_OTP_length
        else:
            parsed_config_profile_details['OTP_length'] = each_config_profile_details.get('OTP_length')

        return parsed_config_profile_details



    def parse_timer_based_config_detail(self, each_config_profile_details):
        parsed_config_profile_details = dict()

        parsed_config_profile_details['OTP_type'] = each_config_profile_details.get('OTP_type')
        parsed_config_profile_details['OTP_usage'] = each_config_profile_details.get('OTP_usage')

        if each_config_profile_details.get('expire_after') == None:
            parsed_config_profile_details['expire_after'] = self.default_expire_after
        else:
            parsed_config_profile_details['expire_after'] = each_config_profile_details.get('expire_after')

        if each_config_profile_details.get('OTP_length') == None:
            parsed_config_profile_details['OTP_length'] = self.default_OTP_length
        else:
            parsed_config_profile_details['OTP_length'] = each_config_profile_details.get('OTP_length')

        return parsed_config_profile_details


        
    def _get_config_based_on_OTP_config_profile_name(self, OTP_config_name):
        if OTP_config_name in self.config_profiles.keys():
            return self.config_profiles.get(OTP_config_name)
        else:
            raise Exception('No configuration exists with this name.')