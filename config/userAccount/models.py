import os
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from extentions.regexValidators.phone_number_validator import PhoneNumberValidator
from django.apps import apps
from django.contrib.auth.hashers import make_password
# Create your models here.





class CustomUserManager(BaseUserManager):
    def _create_user(self, first_name, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given first name, phone number, email, and password.
        """
        if not first_name:
            raise ValueError("The given first name must be set")
        if not phone_number:
            raise ValueError("The given phone number must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(first_name=first_name, phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    

    def create_user(self, first_name, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(first_name, phone_number, email, password, **extra_fields)
    

    def create_superuser(self, first_name, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_account_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(first_name, phone_number, email, password, **extra_fields)





class UserAccount(AbstractUser):
    first_name              = models.CharField(max_length=50, verbose_name='First Name', blank=False, null=False)
    last_name               = models.CharField(max_length=50, verbose_name='Last Name', blank=True, null=True)
    # username                = models.CharField(max_length=50, verbose_name='Username', blank=False, null=False, validators=[ASCIIUsernameValidator])
    username                = None
    phone_number            = models.CharField(max_length=11, verbose_name='Phone Number',unique=True, blank=False, null=False, validators=[PhoneNumberValidator])
    email                   = models.EmailField(unique=True, blank=False, null=False, verbose_name='Email')
    is_account_verified     = models.BooleanField(default=False, verbose_name='Is Account Verified?')
    new_phone_number        = models.CharField(max_length=11, verbose_name='New Unverified Phone Number', blank=True, null=True, validators=[PhoneNumberValidator])
    is_new_phone_verified   = models.BooleanField(default=True, verbose_name='Is New Phone Number Verified?')


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'email']


    objects = CustomUserManager()


    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'


    def __str__(self):
        return str(self.phone_number)





def set_filename(instance, filename):
    splittedFileName = filename.split('.')
    extention = splittedFileName[-1]
    filename = '.'.join(splittedFileName[0:(len(splittedFileName)-1)])
    filename = filename + '__' + str(timezone.now().timestamp())
    filePath = "user_{0}/{1}.{2}".format(instance.user.pk, filename, extention)
    return os.path.join('profile_photo', filePath)



class UserAccountProfilePicture(models.Model):
    user            = models.ForeignKey('UserAccount', on_delete=models.CASCADE, related_name='photos', verbose_name='User Account Profile Picture')
    photo           = models.ImageField(upload_to=set_filename, blank=False, null=False, verbose_name='Profile Picture')
    is_default_pic  = models.BooleanField(default=True, blank=False, null=False, verbose_name='Is It Default Profile Picture?')
    creation_date   = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='This Profile Picture\'s Creation Date')


    class Meta:
        verbose_name = 'User Account Profile Picture'
        verbose_name_plural = 'User Account Profile Pictures'


    def __str__(self):
        return str(self.user) + "'s profile picture -- " + str(self.creation_date)
