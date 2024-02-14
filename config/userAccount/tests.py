from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.db.models import Q
from otp.models import OTPCode
from django.contrib.auth.hashers import make_password
from .user_account_OTP_manager import UserAccountOTPManager
# Create your tests here.



class UserAccountTests(APITestCase):
    maxDiff = None

    def setUp(self):
        # Setup run before every test method.
        pass





    def tearDown(self):
        # Clean up run after every test method.
        pass





    def test_user_account_creation_1(self):
        # Testing normal users' user creation.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        response = self.client.post(url, data, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)

        created_user = UserModel.objects.all()[0]
        self.assertEqual(created_user.first_name, "test user")
        self.assertEqual(created_user.last_name, "test user")
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.email, "testuser@mail.com")
        self.assertNotEqual(created_user.password,None)
        self.assertNotEqual(created_user.password, "test_user_12345")
        self.assertEqual(created_user.is_active, False)
        self.assertEqual(created_user.is_account_verified, False)
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)

        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))
        self.assertEqual(OTP_code_object.user, created_user)
        self.assertNotEqual(OTP_code_object.otp, None)
        self.assertEqual(OTP_code_object.otp.isdigit(), True)
        self.assertEqual(len(OTP_code_object.otp), UserAccountOTPManager.config['default_OTP_length'])
        self.assertEqual(OTP_code_object.otp_type, UserAccountOTPManager.config['config_profiles']['account_verification']['OTP_type'])
        self.assertEqual(OTP_code_object.otp_usage, UserAccountOTPManager.config['config_profiles']['account_verification']['OTP_usage'])
        self.assertNotEqual(OTP_code_object.otp_creation_date, None)
        self.assertEqual(OTP_code_object.expire_after, UserAccountOTPManager.config['default_expire_after'])
        self.assertEqual(OTP_code_object.try_counter, 0)
        self.assertEqual(OTP_code_object.max_possible_try, UserAccountOTPManager.config['config_profiles']['account_verification']['max_possible_try'])





    def test_user_account_creation_2(self):
        # Testing superusers' user creation. -- This way, no account verification otp object will be generated.
        UserModel = get_user_model()


        # Creating superuser
        superuser_object = UserModel.objects.create(
            first_name="super user",
            last_name="super_user",
            phone_number="09378889900",
            email="superuser@mail.com",
            password= make_password("test_user_12345"),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            is_account_verified=True
        )


        # Authenticating superuser
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378889900",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Creating normal user by superuser.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 2)

        created_user = UserModel.objects.get(phone_number="09378884433")
        self.assertEqual(created_user.first_name, "test user")
        self.assertEqual(created_user.last_name, "test user")
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.email, "testuser@mail.com")
        self.assertNotEqual(created_user.password,None)
        self.assertNotEqual(created_user.password, "test_user_12345")
        self.assertEqual(created_user.is_active, True)
        self.assertEqual(created_user.is_account_verified, True)
        self.assertEqual(created_user.is_superuser, True)
        self.assertEqual(created_user.is_staff, True)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)





    def test_user_account_creation_3(self):
        # Testing user creation when data has problem (duplicate data).
        UserModel = get_user_model()


        # Creating normal user 1
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Creating normal user 2
        data = {
            'first_name': "test user 2",
            'last_name': "test user 2",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345"
        }
        response = self.client.post(url, data, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        model_verbose_name = UserModel._meta.verbose_name.title()
        phone_number_verbose_name = UserModel._meta.get_field('phone_number').verbose_name.title()
        self.assertEqual(response.data['phone_number'][0], model_verbose_name + " with this " + phone_number_verbose_name + " already exists.")

        email_verbose_name = UserModel._meta.get_field('email').verbose_name.title()
        self.assertEqual(response.data['email'][0], model_verbose_name + " with this " + email_verbose_name + " already exists.")





    def test_user_account_verification_1(self):
        # Testing user verification.
        UserModel = get_user_model()


        # Creating normal user
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.all()[0]
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {'OTP': 'Account verified.'})

        created_user = UserModel.objects.all()[0]
        self.assertEqual(created_user.first_name, "test user")
        self.assertEqual(created_user.last_name, "test user")
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.email, "testuser@mail.com")
        self.assertNotEqual(created_user.password, None)
        self.assertNotEqual(created_user.password, "test_user_12345")
        self.assertEqual(created_user.is_active, True)
        self.assertEqual(created_user.is_account_verified, True)
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)

        OTP_code_objects = OTPCode.objects.all()
        self.assertEqual(len(OTP_code_objects), 0)





    def test_user_account_update_1(self):
        # Testing normal users' user update without changing phone number.
        UserModel = get_user_model()


        # Creating normal user
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.all()[0]
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user.
        created_user = UserModel.objects.all()[0]
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884433",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884433",
            'email': "updatedtestuser@mail.com",
            'is_superuser': "True",
            'is_active': "False",
            'is_account_verified': "False",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }


        # Validating results.
        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_user = UserModel.objects.all()[0]
        self.assertEqual(created_user.first_name, "updated test user")
        self.assertEqual(created_user.last_name, "updated test user")
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.email, "updatedtestuser@mail.com")
        self.assertEqual(created_user.is_active, True)
        self.assertEqual(created_user.is_account_verified, True)
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)





    def test_user_account_update_2(self):
        # Testing superusers' user update without changing phone number.
        UserModel = get_user_model()


        # Creating superuser
        superuser_object = UserModel.objects.create(
            first_name="super user",
            last_name="super_user",
            phone_number="09378889900",
            email="superuser@mail.com",
            password= make_password("test_user_12345"),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            is_account_verified=True
        )


        # Creating normal user
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884433")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating user. -- superuser login
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378889900",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user by superuser.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884433",
            'email': "updatedtestuser@mail.com",
            'is_superuser': "True",
            'is_active': "False",
            'is_account_verified': "False",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_user = UserModel.objects.get(phone_number="09378884433")
        self.assertEqual(created_user.first_name, "updated test user")
        self.assertEqual(created_user.last_name, "updated test user")
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.email, "updatedtestuser@mail.com")
        self.assertEqual(created_user.is_active, False)
        self.assertEqual(created_user.is_account_verified, False)
        self.assertEqual(created_user.is_superuser, True)
        self.assertEqual(created_user.is_staff, True)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)







    def test_user_account_update_3(self):
        # Testing normal users' user phone number update.
        UserModel = get_user_model()


        # Creating normal user
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.all()[0]
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user.
        created_user = UserModel.objects.all()[0]
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884433",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884455",
            'email': "updatedtestuser@mail.com",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }

        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_user = UserModel.objects.all()[0]        
        self.assertEqual(created_user.first_name, "updated test user")
        self.assertEqual(created_user.last_name, "updated test user")
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.email, "updatedtestuser@mail.com")
        self.assertEqual(created_user.is_active, True)
        self.assertEqual(created_user.is_account_verified, True)
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        self.assertEqual(created_user.new_phone_number, "09378884455")
        self.assertEqual(created_user.is_new_phone_verified, False)


        OTP_code_object = OTPCode.objects.get(Q(otp_usage='New Phone Number Verification'))
        self.assertEqual(OTP_code_object.user, created_user)
        self.assertNotEqual(OTP_code_object.otp, None)
        self.assertEqual(OTP_code_object.otp.isdigit(), True)
        self.assertEqual(len(OTP_code_object.otp), UserAccountOTPManager.config['default_OTP_length'])
        self.assertEqual(OTP_code_object.otp_type, UserAccountOTPManager.config['config_profiles']['new_phone_number_verification']['OTP_type'])
        self.assertEqual(OTP_code_object.otp_usage, UserAccountOTPManager.config['config_profiles']['new_phone_number_verification']['OTP_usage'])
        self.assertNotEqual(OTP_code_object.otp_creation_date, None)
        self.assertEqual(OTP_code_object.expire_after, None)
        self.assertEqual(OTP_code_object.try_counter, 0)
        self.assertEqual(OTP_code_object.max_possible_try, UserAccountOTPManager.config['default_max_possible_try'])





    def test_user_account_update_4(self):
        # Testing superusers' user phone number update.
        UserModel = get_user_model()


        # Creating superuser
        superuser_object = UserModel.objects.create(
            first_name="super user",
            last_name="super_user",
            phone_number="09378889900",
            email="superuser@mail.com",
            password= make_password("test_user_12345"),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            is_account_verified=True
        )


        # Creating normal user
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345",
            'is_superuser': "True",
            'is_active': "True",
            'is_account_verified': "True",
            'is_staff': "True",
            'new_phone_number': "09378884455",
            'is_new_phone_verified': "False"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884433")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating user. -- superuser login
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378889900",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user by superuser.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884455",
            'email': "updatedtestuser@mail.com",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }

        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_user = UserModel.objects.get(pk=created_user.pk)
        self.assertEqual(created_user.first_name, "updated test user")
        self.assertEqual(created_user.last_name, "updated test user")
        self.assertEqual(created_user.phone_number, "09378884455")
        self.assertEqual(created_user.email, "updatedtestuser@mail.com")
        self.assertEqual(created_user.is_active, True)
        self.assertEqual(created_user.is_account_verified, True)
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)





    def test_user_account_update_5(self):
        # Testing if a normal users' can update another user's data.
        UserModel = get_user_model()


        # Creating normal user 1
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Creating normal user 2
        data = {
            'first_name': "test user 2",
            'last_name': "test user 2",
            'phone_number': "09378884422",
            'email': "testuser2@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user 1.
        created_user_1 = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user_1.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Verifying normal user 2.
        created_user_2 = UserModel.objects.get(phone_number="09378884422")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884422'))

        url = reverse('verify-account', kwargs={'userPK': created_user_2.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884411",
            "password": "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user 2 by normal user 1.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user_2.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884455",
            'email': "updatedtestuser@mail.com",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }

        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





    def test_user_account_new_phone_number_verification_1(self):
        # Testing normal users' user phone number update.
        UserModel = get_user_model()


        # Creating normal user
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user",
            'last_name': "test user",
            'phone_number': "09378884433",
            'email': "testuser@mail.com",
            'password': "test_user_12345",
            'confirm_password': "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.all()[0]
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        # Authenticating normal user.
        created_user = UserModel.objects.all()[0]
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884433",
            "password": "test_user_12345"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884455",
            'email': "updatedtestuser@mail.com",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.put(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_user = UserModel.objects.all()[0]
        self.assertEqual(created_user.phone_number, "09378884433")
        self.assertEqual(created_user.new_phone_number, "09378884455")
        self.assertEqual(created_user.is_new_phone_verified, False)


        # Verifying new phone number.
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='New Phone Number Verification'))
        url = reverse('verify-new-phone-number', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Validating results.
        created_user = UserModel.objects.all()[0]
        OTP_code_objects = OTPCode.objects.filter(Q(otp_usage='New Phone Number Verification'))
        self.assertEqual(len(OTP_code_objects), 0)
        self.assertEqual(created_user.first_name, "updated test user")
        self.assertEqual(created_user.last_name, "updated test user")
        self.assertEqual(created_user.phone_number, "09378884455")
        self.assertEqual(created_user.email, "updatedtestuser@mail.com")
        self.assertEqual(created_user.is_active, True)
        self.assertEqual(created_user.is_account_verified, True)
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        self.assertEqual(created_user.new_phone_number, None)
        self.assertEqual(created_user.is_new_phone_verified, True)





    def test_user_account_new_phone_number_verification_2(self):
        # Testing if a normal users' can verify another user's phone number.
        UserModel = get_user_model()


        # Creating normal user 1
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Creating normal user 2
        data = {
            'first_name': "test user 2",
            'last_name': "test user 2",
            'phone_number': "09378884422",
            'email': "testuser2@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user 1.
        created_user_1 = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user_1.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Verifying normal user 2.
        created_user_2 = UserModel.objects.get(phone_number="09378884422")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884422'))

        url = reverse('verify-account', kwargs={'userPK': created_user_2.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user 1.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884411",
            "password": "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user 1
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user_1.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884455",
            'email': "updatedtestuser@mail.com",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }

        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user 2.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884422",
            "password": "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Verifying new phone number by normal user 2.
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='New Phone Number Verification'))
        url = reverse('verify-new-phone-number', kwargs={'userPK': created_user_1.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }

        response = self.client.post(url, data=data, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





    def test_user_account_request_new_new_phone_number_verification_otp_1(self):
        # Requesting new new phone numer verification otp.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user_1 = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user_1.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884411",
            "password": "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Updating normal user.
        url = reverse('UserAccount-detail', kwargs={'userPK': created_user_1.pk})
        data = {
            'first_name': "updated test user",
            'last_name': "updated test user",
            'phone_number': "09378884455",
            'email': "updatedtestuser@mail.com",
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }

        response = self.client.put(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Requesting new new phone numer verification otp.
        url = reverse('request-new-new-phone-number-verification-OTP', kwargs={'userPK': created_user_1.pk})
        response = self.client.post(url, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_account_request_new_phone_number_verification_otp_2(self):
        # Requesting new new phone numer verification otp when phone number didn't changed so no previous otp code object exists.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user_1 = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user_1.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884411",
            "password": "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        url = reverse('request-new-new-phone-number-verification-OTP', kwargs={'userPK': created_user_1.pk})
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, headers=headers, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





    def test_user_account_change_password_1(self):
        # Testing if a normal users' can change password
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Authenticating normal user.
        url = reverse('token_obtain_pair')
        data = {
            "phone_number": "09378884411",
            "password": "test_user_12345_@@"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # changing normal user password.
        url = reverse('change-password', kwargs={'userPK': created_user.pk})
        data = {
            'old_password': "test_user_12345_@@",
            'new_password': "new_test_user_password_12345_@@",
            'confirm_new_password': "new_test_user_password_12345_@@"
        }
        headers = {
            "Authorization": "Bearer " + response.data['access']
        }
        response = self.client.post(url, data=data, headers=headers, format='json')

    
        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_user_account_request_reset_password_otp_1(self):
        # Requesting password reset otp for a user.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # requesting password reset otp for normal user.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09378884411"
        }
        response = self.client.post(url, data, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Forgotten Password'))
        self.assertEqual(OTP_code_object.user, created_user)
        self.assertNotEqual(OTP_code_object.otp, None)
        self.assertEqual(OTP_code_object.otp.isdigit(), True)
        self.assertEqual(len(OTP_code_object.otp), UserAccountOTPManager.config['default_OTP_length'])
        self.assertEqual(OTP_code_object.otp_type, UserAccountOTPManager.config['config_profiles']['reset_password']['OTP_type'])
        self.assertEqual(OTP_code_object.otp_usage, UserAccountOTPManager.config['config_profiles']['reset_password']['OTP_usage'])
        self.assertNotEqual(OTP_code_object.otp_creation_date, None)
        self.assertEqual(OTP_code_object.expire_after, UserAccountOTPManager.config['default_expire_after'])
        self.assertEqual(OTP_code_object.try_counter, 0)
        self.assertEqual(OTP_code_object.max_possible_try, UserAccountOTPManager.config['default_max_possible_try'])





    def test_user_account_request_reset_password_otp_2(self):
        # Requesting password reset otp for a user which does not exists.


        # requesting password reset otp for a user which does not exist.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09370004411"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        OTP_code_object = OTPCode.objects.filter(Q(otp_usage='Forgotten Password'))


        # Validating results.
        self.assertEqual(len(OTP_code_object), 0)





    def test_user_account_request_reset_password_otp_3(self):
        # Requesting password reset otp when user is inactivated.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Making normal user inactive.
        created_user = UserModel.objects.get(phone_number="09378884411")
        created_user.is_active = False
        created_user.save()


        # Requesting password reset otp for normal user.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09378884411"
        }
        response = self.client.post(url, data, format='json')


        # Validating results.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        OTP_code_object = OTPCode.objects.filter(Q(otp_usage='Forgotten Password'))
        self.assertEqual(len(OTP_code_object), 0)





    def test_user_account_verify_reset_password_otp_1(self):
        # Testing verifying reset password otp.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Requesting password reset otp for normal user.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09378884411"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Verifying reset password otp.
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Forgotten Password'))
        reset_password_url = reverse('verify-reset-password-OTP')
        reset_password_data = {
            "otp": OTP_code_object.otp
        }
        reset_password_response = self.client.post(reset_password_url, reset_password_data, format='json')
        
        
        # Validating results.
        self.assertEqual(reset_password_response.status_code, status.HTTP_200_OK)





    def test_user_account_verify_reset_password_otp_2(self):
        # Testing verifying reset password otp when code does not exist.


        # Verifying reset password otp.
        reset_password_url = reverse('verify-reset-password-OTP')
        reset_password_data = {
            "otp": "9876543210"
        }
        reset_password_response = self.client.post(reset_password_url, reset_password_data, format='json')


        # Validating results.
        self.assertEqual(reset_password_response.status_code, status.HTTP_404_NOT_FOUND)





    def test_user_account_verify_reset_password_otp_3(self):
        # Testing verifying reset password otp when user is inactived.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Requesting password reset otp for normal user.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09378884411"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Making normal user inactivate.
        created_user = UserModel.objects.get(phone_number="09378884411")
        created_user.is_active = False
        created_user.save()


        # Verifying otp.
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Forgotten Password'))
        reset_password_url = reverse('verify-reset-password-OTP')
        reset_password_data = {
            "otp": OTP_code_object.otp
        }
        reset_password_response = self.client.post(reset_password_url, reset_password_data, format='json')


        # Validating results.
        self.assertEqual(reset_password_response.status_code, status.HTTP_403_FORBIDDEN)





    def test_user_account_reset_password_otp_1(self):
        # Testing reseting password.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Requesting password reset otp for user 1.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09378884411"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Reseting password with otp.
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Forgotten Password'))
        reset_password_url = reverse('reset-password')
        reset_password_data = {
            "otp": OTP_code_object.otp,
            "new_password": "test_user_12345_##",
            "confirm_new_password": "test_user_12345_##"
        }
        reset_password_response = self.client.post(reset_password_url, reset_password_data, format='json')
        
        
        # Validating results.
        self.assertEqual(reset_password_response.status_code, status.HTTP_200_OK)






    def test_user_account_reset_password_otp_2(self):
        # Testing reseting password when user is inactivated.
        UserModel = get_user_model()


        # Creating normal user.
        url = reverse('UserAccount-list')
        data = {
            'first_name': "test user 1",
            'last_name': "test user 1",
            'phone_number': "09378884411",
            'email': "testuser1@mail.com",
            'password': "test_user_12345_@@",
            'confirm_password': "test_user_12345_@@",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Verifying normal user.
        created_user = UserModel.objects.get(phone_number="09378884411")
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Account Verification') & Q(user__phone_number='09378884411'))

        url = reverse('verify-account', kwargs={'userPK': created_user.pk})
        data = {
            'otp': OTP_code_object.otp
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Requesting password reset otp for normal user.
        url = reverse('request-reset-password-OTP')
        data = {
            "phone_number": "09378884411"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Making normal user inactive.
        created_user = UserModel.objects.get(phone_number="09378884411")
        created_user.is_active = False
        created_user.save()


        # Reseting password with otp.
        OTP_code_object = OTPCode.objects.get(Q(otp_usage='Forgotten Password'))
        reset_password_url = reverse('reset-password')
        reset_password_data = {
            "otp": OTP_code_object.otp,
            "new_password": "test_user_12345_##",
            "confirm_new_password": "test_user_12345_##"
        }
        reset_password_response = self.client.post(reset_password_url, reset_password_data, format='json')


        # Validating results.
        self.assertEqual(reset_password_response.status_code, status.HTTP_403_FORBIDDEN)




