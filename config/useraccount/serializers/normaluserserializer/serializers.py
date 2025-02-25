from useraccount.models import UserAccount, UserAccountProfilePicture
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.core import exceptions
from django.db.models import Q


class UserAccountCreationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pk'].read_only = True
        self.fields['password'].write_only = True
        self.fields['is_active'].read_only = True
        self.fields['is_account_verified'].read_only = True

    confirm_password = serializers.CharField(style = {'input_type': 'password'}, label='Repeated Password', write_only=True)

    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'confirm_password', 'last_login', 'is_active', 'date_joined', 'is_account_verified']


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
        
        # if self.request.data.get('is_account_verified') == None or self.request.data.get('is_account_verified') == '':
        #     attrs['is_account_verified'] = False
        return super().validate(attrs)

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(password=self.validated_data.get('password'))
        return super().save(**kwargs)





class UserAccountUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pk'].read_only = True
        self.fields['new_phone_number'].read_only = True
        self.fields['is_new_phone_verified'].read_only = True
        self.fields['confirm_password'] = serializers.CharField(style = {'input_type': 'password'}, label='Repeated Password', write_only=True)

    class Meta:
        model = UserAccount
        fields = ['pk', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'last_login', 'date_joined', 'new_phone_number', 'is_new_phone_verified']


    def validate(self, attrs):
        if attrs.get('phone_number', None) != None:
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
        self.requested_user = self.context.get('requested_user')

        fields = ['pk', 'photos', 'first_name', 'last_name', 'username']
        if self.user.is_authenticated and str(self.user) == str(self.requested_user):
            fields = ['pk', 'photos', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'last_login', 'new_phone_number', 'is_new_phone_verified', 'date_joined']


        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

    photos = serializers.PrimaryKeyRelatedField(queryset=UserAccountProfilePicture.objects.all(), many=True)

    class Meta:
        model = UserAccount
        fields = ['pk', 'photos', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'last_login', 'date_joined', 'new_phone_number', 'is_new_phone_verified']





class UserAccountProfilePictureCreationRetrivalSerializer(serializers.ModelSerializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['pk'].read_only = True
        self.fields['user'].read_only = True
        self.fields['user'].required = False
        self.fields['creation_date'].read_only = True
        self.fields['creation_date'].required = False

    class Meta:
        model = UserAccountProfilePicture
        fields = ['pk', 'user', 'photo', 'is_default_pic', 'creation_date']


    def validate(self, attrs):
        if self.request.data.get('is_default_pic') == None or self.request.data.get('is_default_pic') == '':
            attrs['is_default_pic'] = True
        return attrs





class UserAccountProfilePictureUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['pk'].read_only = True
        self.fields['photo'].read_only = True
        self.fields['photo'].required = True
        self.fields['user'].read_only = True
        self.fields['user'].required = False
        self.fields['creation_date'].read_only = True
        self.fields['creation_date'].required = False

    class Meta:
        model = UserAccountProfilePicture
        fields = ['pk', 'user', 'photo', 'is_default_pic', 'creation_date']


    def validate(self, attrs):
        if self.request.data.get('is_default_pic') == None or self.request.data.get('is_default_pic') == '':
            attrs['is_default_pic'] = True
        return attrs
