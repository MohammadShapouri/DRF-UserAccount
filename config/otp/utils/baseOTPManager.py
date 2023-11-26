from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from otp.models import OTPCode
from random import randint
from .baseOTPConfigManager import BaseOTPConfigManager


UserModel = get_user_model()



class BaseOTPManager(BaseOTPConfigManager):
    
    OTPCodeObject = None
    config = {
            'defaultOTPLength': 8, 
            'defaultMaxPossibleTry': 5,
            'defaultExpireAfter': 60,
            'configProfiles': {
            'account_verification':{
                'OTPType': 'timer_counter_based',
                'OTPUsage': 'Account Verification',
            },
            'new_phone_number_verification': {
                'OTPType': 'counter_based',
                'OTPUsage': 'New Phone Number Verification',
            },
            'reset_password': {
                'OTPType': 'timer_based',
                'OTPUsage': 'Forgotten Password',
            }
            }
        }

    def getConfig(self):
        self._createConfig(self.config)



    def afterOTPVerificationAction(self, user):
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
        # allowedChars = string.digits
        # return int(''.join(random.choices(allowedChars, k=charCount)))
        rangeStart = 10**(charCount-1)
        rangeEnd = (10**charCount)-1
        return str(randint(rangeStart, rangeEnd))



    def OTPQuery(self, user, OTPType, OTPUsage):
        # In case you have more than one object of a specific otp for any reason.
        OTPCodeObjects = OTPCode.objects.filter(Q(user = user) & Q(otp_type = OTPType) & Q(otp_usage = OTPUsage))
        if len(OTPCodeObjects) > 1:
            isFirstRound = True
            for i in range(len(OTPCodeObjects)):
                if isFirstRound == True:
                    latestCreationDate = OTPCodeObjects[i].otp_creation_date
                    self.OTPCodeObject = OTPCodeObjects[i]
                    isFirstRound = False
                    continue
                if latestCreationDate < OTPCodeObjects[i].otp_creation_date:
                    latestCreationDate = OTPCodeObjects[i].otp_creation_date
                    self.OTPCodeObject = OTPCodeObjects[i]

            for i in range(len(OTPCodeObjects)):
                if self.OTPCodeObject.pk != OTPCodeObjects[i].pk:
                    OTPCodeObjects[i].delete()
        elif len(OTPCodeObjects) == 1:
            self.OTPCodeObject = OTPCodeObjects[0]



    def generateOTP(self, user, OTPConfigName):
        config = self.getConfigBasedOnOTPUsage(OTPConfigName)
        self.OTPQuery(user, config['OTPType'], config['OTPUsage'])

        if config['OTPType'] == "timer_counter_based":
            return self.generateTimerAndCounterBasedOTP(self.OTPCodeObject, user, config['OTPType'], config['OTPUsage'], config['OTPLength'], config['maxPossibleTry'], config['expireAfter'])
        elif config['OTPType'] == "counter_based":
            return self.generateCounterBasedOTP(self.OTPCodeObject, user, config['OTPType'], config['OTPUsage'], config['OTPLength'], config['maxPossibleTry'])
        elif config['OTPType'] == "timer_based":
            return self.generateTimerBasedOTP(self.OTPCodeObject, user, config['OTPType'], config['OTPUsage'], config['OTPLength'], config['expireAfter'])

    

    def generateTimerAndCounterBasedOTP(self, OTPCodeObject, user, OTPType, OTPUsage, OTPLength, maxPossibleTry, expireAfter):
        if OTPCodeObject is None:
            OTPCodeObject = OTPCode.objects.create(user = user, 
                                                   otp = self.createRandomDigits(OTPLength),
                                                   otp_type = OTPType, 
                                                   otp_usage = OTPUsage, 
                                                   max_possible_try = maxPossibleTry,
                                                    expire_after = expireAfter)
        else:
            OTPCodeObject.otp = self.createRandomDigits(OTPLength)
            OTPCodeObject.otp_usage = OTPUsage
            OTPCodeObject.max_possible_try = maxPossibleTry
            OTPCodeObject.expire_after = expireAfter
            OTPCodeObject.last_try = None
            OTPCodeObject.otp_creation_date = timezone.now()
            OTPCodeObject.save()
        return OTPCodeObject

    

    def generateCounterBasedOTP(self, OTPCodeObject, user, OTPType, OTPUsage, OTPLength, maxPossibleTry):
        if OTPCodeObject is None:
            OTPCodeObject = OTPCode.objects.create(user = user, 
                                                   otp = self.createRandomDigits(OTPLength),
                                                   otp_type = OTPType, 
                                                   otp_usage = OTPUsage, 
                                                   max_possible_try = maxPossibleTry)
        else:
            OTPCodeObject.otp = self.createRandomDigits(OTPLength)
            OTPCodeObject.otp_usage = OTPUsage
            OTPCodeObject.max_possible_try = maxPossibleTry
            OTPCodeObject.last_try = None
            OTPCodeObject.otp_creation_date = timezone.now()
            OTPCodeObject.save()
        return OTPCodeObject



    def generateTimerBasedOTP(self, OTPCodeObject, user, OTPType, OTPUsage, OTPLength, expireAfter):
        if OTPCodeObject is None:
            OTPCodeObject = OTPCode.objects.create(user = user, 
                                                   otp = self.createRandomDigits(OTPLength),
                                                   otp_type = OTPType, 
                                                   otp_usage = OTPUsage,
                                                   expire_after = expireAfter)
        else:
            OTPCodeObject.otp = self.createRandomDigits(OTPLength)
            OTPCodeObject.otp_usage = OTPUsage
            OTPCodeObject.expire_after = expireAfter
            OTPCodeObject.last_try = None
            OTPCodeObject.otp_creation_date = timezone.now()
            OTPCodeObject.save()
        return OTPCodeObject



    def verifyOTP(self, user, OTPConfigName, userInputCode):
        """
        If verification is successful, it automatically calls afterOTPVerificationAction
        and passes related object to it.
        """
        config = self.getConfigBasedOnOTPUsage(OTPConfigName)
        self.OTPQuery(user, config['OTPType'], config['OTPUsage'])

        if config['OTPType'] == "timer_counter_based":
            return self.verifyTimerAndCounterBasedOTP(user, userInputCode)
        elif config['OTPType'] == "counter_based":
            return self.verifyCounterBasedOTP(user, userInputCode)
        elif config['OTPType'] == "timer_based":
            return self.verifyTimerBasedOTP(user, userInputCode)



    def verifyTimerAndCounterBasedOTP(self, user, userInputCode):
        if self.OTPCodeObject.hasTime() == True:
            if self.OTPCodeObject.canTry() == True:
                if self.OTPCodeObject.otp == userInputCode:
                    self.OTPCodeObject.delete()
                    return self.afterOTPVerificationAction(user)
                else:
                    self.OTPCodeObject.incrementTryCounterValue()
                    return self.wrongOTPInput()
            else:
                return self.tooManyTries()
        else:
            return self.OTPExpired()



    def verifyCounterBasedOTP(self, user, userInputCode):
        if self.OTPCodeObject.canTry() == True:
            if self.OTPCodeObject.otp == userInputCode:
                self.OTPCodeObject.delete()
                return self.afterOTPVerificationAction(user)
            else:
                self.OTPCodeObject.incrementTryCounterValue()
                return self.wrongOTPInput()
        else:
            return self.tooManyTries()
        


    def verifyTimerBasedOTP(self, user, userInputCode):
        if self.OTPCodeObject.hasTime == True:
            if self.OTPCodeObject.otp == userInputCode:
                self.OTPCodeObject.delete()
                return  self.afterOTPVerificationAction(user)
            else:
                self.OTPCodeObject.incrementTryCounterValue()
                return self.wrongOTPInput()
        else:
            return self.OTPExpired()
        


    def getConfigBasedOnOTPUsage(self, OTPConfigName):
        self.getConfig()
        return self._getConfigBasedOnOTPUsage(OTPConfigName)



    def getOTPModelObjectByUserInputCode(self, userInputCode, OTPConfigName=None):
        try:
            config = self.getConfigBasedOnOTPUsage(OTPConfigName)
            return OTPCode.objects.get(Q(otp_usage=config['OTPUsage']) & Q(otp=userInputCode))
        except OTPCode.DoesNotExist:
            return None
        # config = self.getConfigBasedOnOTPUsage(OTPConfigName)
        # OTPCodeObject = OTPCode.objects.filter(Q(otp_usage=config['OTPUsage']) & Q(otp=userInputCode))
        # if len(OTPCodeObject) > 0:
        #     return OTPCodeObject[0]
        # return None
        

    def getOTPModelObjectByUserId(self, userId, OTPConfigName=None):
        try:
            config = self.getConfigBasedOnOTPUsage(OTPConfigName)
            return OTPCode.objects.get(Q(otp_usage=config['OTPUsage']) & Q(pk=userId))
        except OTPCode.DoesNotExist:
            return None
        # config = self.getConfigBasedOnOTPUsage(OTPConfigName)
        # OTPCodeObject = OTPCode.objects.filter(Q(otp_usage=config['OTPUsage']) & Q(pk=userId))
        # if len(OTPCodeObject) > 0:
        #     return OTPCodeObject[0]
        # return None