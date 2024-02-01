from rest_framework import serializers
from rest_framework import exceptions as rest_exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserAccount, UserAccountProfilePicture
from .user_account_OTP_manager import UserAccountOTPManager
from otp.utils.acceptable_OTP_values import least_acceptable_OTP_length, most_acceptable_OTP_length
from extentions.regexValidators.phone_number_validator import PhoneNumberValidator
from rest_framework import status
from .tasks import send_SMS





class UserAccountCreationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pk'].read_only = True
        self.user = self.context.get('user')
        self.fields['password'].write_only = True
        
        if self.user.is_authenticated and self.user.is_superuser or self.user.is_staff:
            # 'groups' and 'user_permissions' are still not added.
            fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified']
        else:
            self.fields['is_active'].read_only = True
            self.fields['is_account_verified'].read_only = True
            fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password', 'is_active', 'is_account_verified']
        
        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

    confirm_password = serializers.CharField(style = {'input_type': 'password'}, label='Repeated Password', write_only=True)

    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']


    def validate(self, attrs):
        # Get passwords from data.
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')
        errors_dict = dict()

        if password != confirm_password:
            errors_dict['password'] = "Two passwords aren't the same."
        # Here data has all the fields which have validated values.
        # So we can create a User instance out of it.
        user = UserAccount(**attrs)
        try:
            # Validate the password and catch the exception
            validate_password(password=password, user=user)
        # The exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors_dict['password'] = list(e.messages)
        if errors_dict:
            raise serializers.ValidationError(errors_dict)
        return super().validate(attrs)

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(password=self.validated_data.get('password'))
        return super().save(**kwargs)





class UserAccountUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pk'].read_only = True
        self.user = self.context.get('user')
        self.fields['confirm_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Repeated Password', write_only=True)


        if self.user.is_authenticated and self.user.is_superuser or self.user.is_staff:
            # 'groups' and 'user_permissions' are still not added.
            fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified']
        else:
            self.fields['new_phone_number'].read_only = True
            self.fields['is_new_phone_verified'].read_only = True
            fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'new_phone_number', 'is_new_phone_verified']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)


    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']


    def validate(self, attrs):
        if attrs['phone_number'] != self.instance.phone_number:
            new_phone_number = attrs['phone_number']
            user = UserAccount.objects.filter(~Q(pk=self.instance.pk) & Q(new_phone_number = new_phone_number))
            if len(user) > 0:
                model_name = UserAccount._meta.verbose_name.title()
                field_name = UserAccount._meta.get_field('phone_number').verbose_name.title()
                raise serializers.ValidationError({'Phone Number': f"{model_name} with this {field_name} already exists."})
        return super().validate(attrs)



class UserAccountRetrivalSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')
        self.requested_pk = self.context.get('requested_pk')
        
        if self.user.is_authenticated:
            if self.user.is_superuser or self.user.is_staff:
                # 'groups' and 'user_permissions' are still not added.
                fields = ['pk', 'photos', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']
            elif str(self.user.pk) == str(self.requested_pk):
                fields = ['pk', 'photos', 'first_name', 'last_name', 'phone_number', 'email', 'last_login', 'new_phone_number', 'is_new_phone_verified', 'date_joined']
            else:
                fields = ['pk', 'photos', 'first_name', 'last_name']
        else:
            fields = ['pk', 'photos', 'first_name', 'last_name']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

    photos = serializers.PrimaryKeyRelatedField(queryset=UserAccountProfilePicture.objects.all(), many=True)


    class Meta:
        model = UserAccount
        fields = ['pk', 'photos', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']





class ChangePasswordSerializer(serializers.Serializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.user = self.context.get('user')
        self.fields['old_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Old Password', write_only=True)
        self.fields['new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='New Password', write_only=True)
        self.fields['confirm_new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Repeated New Password', write_only=True)


    def validate(self, attrs):
        # Get passwords from data.
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.pop('confirm_new_password')
        errors_dict = dict()

        if not self.user.check_password(old_password):
            errors_dict['old_Password'] = "Your old password was entered incorrectly. Please enter it again."
        if new_password != confirm_new_password:
            errors_dict['new_password'] = "Two passwords aren't the same."

        try:
            # Validate the password and catch the exception
            validate_password(password=new_password, user=self.user)
        # The exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors_dict['new_password'] = list(e.messages)
        if errors_dict:
            raise serializers.ValidationError(errors_dict)
        return super().validate(attrs)


    def save(self, **kwargs):
        self.user.password = make_password(password=self.validated_data.get('new_password'))
        self.user.save()





class UserAccountDeletionSerializer(serializers.Serializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.user = self.context.get('user')
        self.fields['password'] = serializers.CharField(style = {'input_type': 'password'}, label='Old Password', write_only=True)


    def validate(self, attrs):
        # Get password from data.
        password = attrs.get('password')
        if not self.user.check_password(password):
            raise serializers.ValidationError({'password': "Your password was entered incorrectly. Please enter it again."})
        return super().validate(attrs)





class RequestResetPasswordOTPSerializer(serializers.Serializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['phone_number'] = serializers.CharField(required=True, validators=[PhoneNumberValidator], label='Phone Number')





class verifyResetPasswordOTPSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['otp'] = serializers.CharField(required=True, label='OTP Code')

    def validate(self, attrs):
        OTP = attrs.get('otp')
        if str.isdigit(OTP) is False:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must not contain characters."})
        if len(OTP) < least_acceptable_OTP_length:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain at least " + least_acceptable_OTP_length + " characters."})
        if len(OTP) > most_acceptable_OTP_length:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain at most " + most_acceptable_OTP_length + " characters."})
        return super().validate(attrs)





class ResetPasswordSerializer(serializers.Serializer, UserAccountOTPManager):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.OTP_code_object = None
        self.user_object = None
        self.fields['otp'] = serializers.CharField(required=True, label='OTP Code')
        self.fields['new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='New Password', write_only=True)
        self.fields['confirm_new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Confirm Password', write_only=True)



    def validate(self, attrs):
        OTP = attrs.get('otp')
        if len(OTP) < 6:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must contain at least 6 characters."})
        elif str.isdigit(OTP) is False:
            raise serializers.ValidationError({'OTP': "OTP is not valid. It must not contain characters."})


        # Get user account
        self.OTP_code_object = self.get_OTP_model_object_by_user_input_code(attrs['otp'], 'reset_password')
        if self.OTP_code_object != None:
            try:
                self.user_object = self.OTP_code_object.user
            except UserAccount.DoesNotExist:
                raise serializers.ValidationError({'detail': "No userAccount exists for this OTP object."})
        else:
            raise serializers.ValidationError({'detail': "No OTP exists with this code."})
        
        if self.user_object.is_active == False and self.user_object.is_account_verified == False:
            raise serializers.ValidationError({'detail': "Account is not active."}, status.HTTP_403_FORBIDDEN)



        # Get passwords from data.
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.pop('confirm_new_password')
        errors_dict = dict()

        if new_password != confirm_new_password:
            errors_dict['new_password'] = "Two passwords aren't the same."

        try:
            # Validate the password and catch the exception
            validate_password(password=new_password, user=self.user_object)
        # The exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors_dict['new_password'] = list(e.messages)
        if errors_dict:
            raise serializers.ValidationError(errors_dict)
        return super().validate(attrs)


    def save(self, **kwargs):
        self.user_object.password = make_password(password=self.validated_data.get('new_password'))
        self.user_object.save()





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, UserAccountOTPManager):
    authentication_error_messages = [
        {"no_account": "No account found with the given credentials."},
        {"no_active_account": "No active account found with the given credentials."},
        {"no_verified_account": "No verified account found with the given credentials. OTP verification will be sent to your SMS."}
        ]

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = None
        try:
            self.user = UserAccount.objects.get(phone_number = authenticate_kwargs[self.username_field])
        except UserAccount.DoesNotExist:
            raise rest_exceptions.AuthenticationFailed(self.authentication_error_messages[0])
        
        if not self.user.check_password(authenticate_kwargs["password"]):
            raise rest_exceptions.AuthenticationFailed(self.authentication_error_messages[0])

        if self.user.is_account_verified is False:
            OTP = self.generate_OTP(user = self.user,
                                    OTP_config_name = 'account_verification'
                                    )
            send_SMS.delay(OTP.otp)
            raise rest_exceptions.AuthenticationFailed(self.authentication_error_messages[2])
        else:
            if self.user.is_active is False:
                raise rest_exceptions.AuthenticationFailed(self.authentication_error_messages[1])
        return super().validate(attrs)







class UserAccountProfilePictureSerializer(serializers.ModelSerializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        # self.user = self.context.get('user')
        self.request = self.context.get('request')
        if self.request.user.is_authenticated and self.request.user.is_superuser or self.request.user.is_staff:
            self.fields['creation_date'].read_only = False
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                self.fields['user'].required = False
                self.fields['user'].read_only = True
        else:
            self.fields['user'].required = False
            self.fields['user'].read_only = True

            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                self.fields['photo'].read_only = True
                self.fields['is_default_pic'].read_only = True
            else:
                self.fields['photo'].read_only = False
                self.fields['is_default_pic'].read_only = False


    class Meta:
        model = UserAccountProfilePicture
        fields = ['pk', 'user', 'photo', 'is_default_pic', 'creation_date']


    def validate(self, attrs):
        if self.request.data.get('is_default_pic') == None or self.request.data.get('is_default_pic') == '':
            attrs['is_default_pic'] = True
        return attrs
