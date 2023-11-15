from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from otp.models import OTPCode
import string
import random


UserModel = get_user_model()

class OTPManager:
    OTPCodeObject = None


    def afterValidationAction(self, user):
        return self.successfulValidationMsg()


    def noOTPExists(self):
        return Response(data={'OTP': "No OTP Exists. Request OTP again."}, status=status.HTTP_404_NOT_FOUND)


    def tooManyTries(self):
        return Response(data={'OTP': "Too Many Tries. Request OTP again."}, status=status.HTTP_403_FORBIDDEN)


    def wrongOTPInput(self):
        return Response(data={'OTP': "OTP code Is Wrong."}, status=status.HTTP_403_FORBIDDEN)


    def OTPExpired(self):
        return Response(data={'OTP': "OTP Is Expired."}, status=status.HTTP_403_FORBIDDEN)
    
    def successfulValidationMsg(self):
        return Response(data={'OTP': "OTP Is Correct."}, status=status.HTTP_200_OK)


    def createRandomDigits(self, charCount):
        allowedChars = string.digits
        return int(''.join(random.choices(allowedChars, k=charCount)))



    def validateOTPTypeInput(self, otp_type):
        validOTPTypeInputs = ['timer_counter_based', 'counter_based', 'timer_based']
        if otp_type not in validOTPTypeInputs:
            raise ValueError("otp_type: otp_type must be one of %r." % validOTPTypeInputs)



    def validateOTPUsageInput(self, otp_usage):
        validOTPUsageInputs = ['account_verification', 'new_phone_number_verification', 'forget_password', 'OTP_login']
        if otp_usage not in validOTPUsageInputs:
            raise ValueError("otp_usage: otp_usage must be one of %r." % validOTPUsageInputs)



    def generateOTP(self, user, otp_type, otp_usage, max_possible_try, expire_after):
        self.validateOTPTypeInput(otp_type)
        self.validateOTPUsageInput(otp_usage)
        try:
            self.OTPCodeObject = OTPCode.objects.get(Q(user=user) & Q(otp_type=otp_type) & Q(otp_usage=otp_usage))
        except OTPCode.DoesNotExist:
            pass

        if otp_type == "timer_counter_based":
            return self.generateTimerAndCounterBasedOTP(self.OTPCodeObject, user, otp_type, otp_usage, max_possible_try, expire_after)
        elif otp_type == "counter_based":
            return self.generateCounterBasedOTP(self.OTPCodeObject, user, otp_type, otp_usage, max_possible_try)
        elif otp_type == "timer_based":
            return self.generateTimerBasedOTP(self.OTPCodeObject, user, otp_type, otp_usage, expire_after)

    

    def generateTimerAndCounterBasedOTP(self, OTPCodeObject, user, otp_type, otp_usage, max_possible_try, expire_after):
        if OTPCodeObject is None:
            OTPCodeObject = OTPCode.objects.create(user, otp_type, otp_usage, max_possible_try, expire_after)
        else:
            OTPCodeObject.otp_usage = otp_usage
            OTPCodeObject.max_possible_try = max_possible_try
            OTPCodeObject.expire_after = expire_after
            OTPCodeObject.last_try = None
            OTPCodeObject.otp_creation_date = timezone.now()
            OTPCodeObject.save()
        return OTPCodeObject

    

    def generateCounterBasedOTP(self, OTPCodeObject, user, otp_type, otp_usage, max_possible_try):
        if OTPCodeObject is None:
            OTPCodeObject = OTPCode.objects.create(user, otp_type, otp_usage, max_possible_try)
        else:
            OTPCodeObject.otp_usage = otp_usage
            OTPCodeObject.max_possible_try = max_possible_try
            OTPCodeObject.last_try = None
            OTPCodeObject.otp_creation_date = timezone.now()
            OTPCodeObject.save()
        return OTPCodeObject



    def generateTimerBasedOTP(self, OTPCodeObject, user, otp_type, otp_usage, expire_after):
        if OTPCodeObject is None:
            OTPCodeObject = OTPCode.objects.create(user, otp_type, otp_usage, expire_after)
        else:
            OTPCodeObject.otp_usage = otp_usage
            OTPCodeObject.expire_after = expire_after
            OTPCodeObject.last_try = None
            OTPCodeObject.otp_creation_date = timezone.now()
            OTPCodeObject.save()
        return OTPCodeObject



    def verifyOTP(self, user, otp_type, otp_usage, userInputCode):
        self.validateOTPFunctionInput()
        if otp_type == "timer_counter_based":
            return self.verifyTimerAndCounterBasedOTP(user, otp_usage, userInputCode)
        elif otp_type == "counter_based":
            return self.verifyCounterBasedOTP(user, otp_usage, userInputCode)
        elif otp_type == "timer_based":
            return self.verifyTimerBasedOTP(user, otp_usage, userInputCode)



    def verifyTimerAndCounterBasedOTP(self, user, otp_usage, userInputCode):
        self.validateOTPUsageInput(otp_usage)
        try:
            self.OTPCodeObject = OTPCode.objects.get(Q(user=user) & Q(otp_type="timer_counter_based") & Q(otp_usage=otp_usage))
        except OTPCode.DoesNotExist:
            return self.noOTPExists()

        if self.OTPCodeObject.canTry() == True:
            if self.OTPCodeObject.hasTime == True:
                if self.OTPCodeObject.otp == userInputCode:
                    self.OTPCodeObject.delete()
                    return self.afterValidationAction(user)
                else:
                    self.OTPCodeObject.incrementTryCounterValue()
                    return self.wrongOTPInput()
            else:
                return self.OTPExpired()
        else:
            return self.tooManyTries()



    def verifyCounterBasedOTP(self, user, otp_usage, userInputCode):
        self.validateOTPUsageInput(otp_usage)
        try:
            self.OTPCodeObject = OTPCode.objects.get(Q(user=user) & Q(otp_type="counter_based") & Q(otp_usage=otp_usage))
        except OTPCode.DoesNotExist:
            return self.noOTPExists()
        
        if self.OTPCodeObject.canTry() == True:
            if self.OTPCodeObject.otp == userInputCode:
                self.OTPCodeObject.delete()
                return self.afterValidationAction(user)
            else:
                self.OTPCodeObject.incrementTryCounterValue()
                return self.wrongOTPInput()
        else:
            return self.tooManyTries()
        


    def verifyTimerBasedOTP(self, user, otp_usage, userInputCode):
        self.validateOTPUsageInput(otp_usage)
        try:
            self.OTPCodeObject = OTPCode.objects.get(Q(user=user) & Q(otp_type="timer_counter_based") & Q(otp_usage=otp_usage))
        except OTPCode.DoesNotExist:
            return self.noOTPExists()

        if self.OTPCodeObject.hasTime == True:
            if self.OTPCodeObject.otp == userInputCode:
                self.OTPCodeObject.delete()
                return  self.afterValidationAction(user)
            else:
                self.OTPCodeObject.incrementTryCounterValue()
                return self.wrongOTPInput()
        else:
            return self.OTPExpired()
