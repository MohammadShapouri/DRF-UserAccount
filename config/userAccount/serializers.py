from rest_framework import serializers
from rest_framework import exceptions as rest_exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserAccount
from .userAccountOTPManager import UserAccountOTPManager





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
        for fieldname in existing - allowed:
            self.fields.pop(fieldname)

    confirm_password = serializers.CharField(style = {'input_type': 'password'}, label='Repeated Password', write_only=True)

    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']


    def validate(self, attrs):
        # Get passwords from data.
        password = attrs.get('password')
        confirmPassword = attrs.pop('confirm_password')
        errors_dict = dict()

        if password != confirmPassword:
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
        for fieldname in existing - allowed:
            self.fields.pop(fieldname)


    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']


    def validate(self, attrs):
        if attrs['phone_number'] != self.instance.phone_number:
            newPhoneNumber = attrs['phone_number']
            user = UserAccount.objects.filter(~Q(pk=self.instance.pk) & Q(new_phone_number = newPhoneNumber))
            if len(user) > 0:
                modelName = UserAccount._meta.verbose_name.title()
                fieldName = UserAccount._meta.get_field('phone_number').verbose_name.title()
                raise serializers.ValidationError({'Phone Number': f"{modelName} with this {fieldName} already exists."})
                
        return super().validate(attrs)



class UserAccountRetrivalSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')
        self.requested_pk = self.context.get('requested_pk')
        
        if self.user.is_authenticated:
            if self.user.is_superuser or self.user.is_staff:
                # 'groups' and 'user_permissions' are still not added.
                fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']
            elif str(self.user.pk) == str(self.requested_pk):
                fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'last_login', 'new_phone_number', 'is_new_phone_verified', 'date_joined']
            else:
                fields = ['pk', 'first_name', 'last_name']
        else:
            fields = ['pk', 'first_name', 'last_name']

        allowed = set(fields)
        existing = set(self.fields.keys())
        for fieldname in existing - allowed:
            self.fields.pop(fieldname)



    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'is_account_verified', 'new_phone_number', 'is_new_phone_verified']





class ChangePasswordSerializer(serializers.Serializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['old_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Old Password', write_only=True)
        self.fields['new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='New Password', write_only=True)
        self.fields['confirm_new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Repeated New Password', write_only=True)


    def validate(self, attrs):
        # Get passwords from data.
        oldPassword = attrs.get('old_password')
        newPassword = attrs.get('new_password')
        confirmNewPassword = attrs.pop('confirm_new_password')
        errors_dict = dict()

        if not self.instance.check_password(oldPassword):
            errors_dict['old_Password'] = "Your old password was entered incorrectly. Please enter it again."
        if newPassword != confirmNewPassword:
            errors_dict['new_password'] = "Two passwords aren't the same."

        try:
            # Validate the password and catch the exception
            validate_password(password=newPassword, user=self.instance)
        # The exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors_dict['new_password'] = list(e.messages)
        if errors_dict:
            raise serializers.ValidationError(errors_dict)
        return super().validate(attrs)


    # def save(self, **kwargs):
    #     self.instance.password = make_password(password=self.validated_data.get('new_password'))
    #     self.instance.save()





class ResetPasswordSerializer(serializers.Serializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['otp'] = serializers.CharField(required=True, label='OTP Code')
        self.fields['new_password'] = serializers.CharField(style = {'input_type': 'password'}, label='New Password', write_only=True)





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





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, UserAccountOTPManager):
    authentication_error_messages = [
        {"no_account": "No account found with the given credentials."},
        {"no_active_account": "No active account found with the given credentials."},
        {"no_verified_account": "No verified account found with the given credentials."}
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
            OTP = self.generateOTP(user = self.user,
                                    OTPConfigName = 'account_verification'
                                    )
            print(OTP.otp)
            raise rest_exceptions.AuthenticationFailed(self.authentication_error_messages[2])
        else:
            if self.user.is_active is False:
                raise rest_exceptions.AuthenticationFailed(self.authentication_error_messages[1])
        return super().validate(attrs)
