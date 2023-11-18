from django.conf import settings



class BaseOTPConfigManager:
    """
    By passing maxPossibleTry and expireAfter in configProfiles, you can customize them.
    """
    defaultOTPLength = None
    defaultMaxPossibleTry = None
    defaultExpireAfter = None
    configProfiles = None


    def _createConfig(self, config):
        self.configKeyValidator(list(config.keys()))
        self.defaultOTPLength = self.getNumericVariable('defaultOTPLength', config['defaultOTPLength'], 8)
        self.defaultMaxPossibleTry = self.getNumericVariable('defaultMaxPossibleTry', config['defaultMaxPossibleTry'], 3)
        self.defaultExpireAfter = self.getNumericVariable('defaultExpireAfter', config['defaultExpireAfter'], 30)
        self.configProfiles = self.parseConfigProfile(config['configProfiles'])




    def parseConfigProfile(self, configProfiles):
        self.configValidator(configProfiles)
        parsedDict = dict()
        configSubDictList = list(configProfiles.items())
        for eachConfigProfileName, eachConfigProfileDetails in configSubDictList:
            self.eachConfigProfileDetailsValidator(eachConfigProfileDetails)

            if eachConfigProfileDetails['OTPType'] == 'timer_counter_based':
                eachConfigParsedDetails = self.parseTimerCounterBasedConfigDetail(eachConfigProfileDetails)
            elif eachConfigProfileDetails['OTPType'] == 'counter_based':
                eachConfigParsedDetails = self.parseCounterBasedConfigDetail(eachConfigProfileDetails)
            elif eachConfigProfileDetails['OTPType'] == 'timer_based':
                eachConfigParsedDetails = self.parseTimerBasedConfigDetail(eachConfigProfileDetails)
            parsedDict[eachConfigProfileName] = eachConfigParsedDetails
        return parsedDict



    def getNumericVariable(self, target, variable, default):
        settingValue = None
        try:
            settings.OTP.get(target)
        except Exception:
            pass

        if variable == None and default == None and settingValue == None:
            raise ValueError('None is not acceptable, Enter a number as variable, default or setting variable')
        
        self.numericValidator(target, variable)
        self.numericValidator(target, default)
        self.numericValidator(target, settingValue)

        if variable != None:
            return int(variable)
        else:
            if settingValue != None:
                return int(settingValue)
        return int(default)
    


    def numericValidator(self, target, value):
        if value != None:
            value = str(value)
            if str.isdigit(value) == False:
                raise TypeError(f'{target} must be numeric.')
            
            if target == 'OTPLength' or target == 'defaultOTPLength':
                value = int(value)
                if value < 6:
                    raise Exception(f'{target} must contain at least 6 characters.')
                if value > 20:
                    raise Exception(f'{target} must contain at most 20 characters.')
            if target == 'maxPossibleTry' or target == 'defaultMaxPossibleTry':
                value = int(value)
                if value < 1:
                    raise Exception(f'{target} must be at least 1.')
            if target == 'expireAfter' or target == 'defaultExpireAfter':
                value = int(value)
                if value < 20:
                    raise Exception(f'{target} must be at least 20.')




    def configValidator(self, configProfiles):
        configProfilesList = list(configProfiles.values())
        configProfilesKey = list(configProfiles.keys())
        self.configProfilesKeyValidator(configProfilesKey)
        for eachConfigProfileDetails in configProfilesList:
            self.eachConfigProfileDetailsValidator(eachConfigProfileDetails)



    def configProfilesKeyValidator(self, configProfilesKey):
        for eachKey in configProfilesKey:
            if configProfilesKey.count(eachKey) > 1:
                raise KeyError('Can\'t use one key multiple times.')



    def configKeyValidator(self, configKey):
        for eachKey in configKey:
            if configKey.count(eachKey) > 1:
                raise KeyError('Can\'t use one key multiple times.')



    def eachConfigProfileDetailsValidator(self, eachConfigProfileDetails):
        validOTPTypeInputs = ['timer_counter_based', 'counter_based', 'timer_based']
        if eachConfigProfileDetails.get('OTPType') not in validOTPTypeInputs:
            raise ValueError("OTPType: OTPType must be one of %r." % validOTPTypeInputs)
        if eachConfigProfileDetails.get('OTPUsage') == None:
            raise ValueError("OTPUsage: OTPUsage must not be empty")
        if eachConfigProfileDetails.get('maxPossibleTry') != None:
            self.numericValidator('maxPossibleTry', eachConfigProfileDetails.get('maxPossibleTry'))
        if eachConfigProfileDetails.get('expireAfter') != None:
            self.numericValidator('expireAfter', eachConfigProfileDetails.get('expireAfter'))
        if eachConfigProfileDetails.get('OTPLength') != None:
            self.numericValidator('OTPLength', eachConfigProfileDetails.get('OTPLength'))



    def parseTimerCounterBasedConfigDetail(self, eachConfigProfileDetails):
        if eachConfigProfileDetails.get('maxPossibleTry') == None:
            eachConfigProfileDetails['maxPossibleTry'] = self.defaultMaxPossibleTry
        if eachConfigProfileDetails.get('expireAfter') == None:
            eachConfigProfileDetails['expireAfter'] = self.defaultExpireAfter
        if eachConfigProfileDetails.get('OTPLength') == None:
            eachConfigProfileDetails['OTPLength'] = self.defaultOTPLength
        return eachConfigProfileDetails
    

    def parseCounterBasedConfigDetail(self, eachConfigProfileDetails):
        if eachConfigProfileDetails.get('maxPossibleTry') == None:
            eachConfigProfileDetails['maxPossibleTry'] = self.defaultMaxPossibleTry
        if eachConfigProfileDetails.get('expireAfter') != None:
            eachConfigProfileDetails['expireAfter'] = None
        if eachConfigProfileDetails.get('OTPLength') == None:
            eachConfigProfileDetails['OTPLength'] = self.defaultOTPLength
        return eachConfigProfileDetails
        

    def parseTimerBasedConfigDetail(self, eachConfigProfileDetails):
        if eachConfigProfileDetails.get('maxPossibleTry') != None:
            eachConfigProfileDetails['maxPossibleTry'] = 0
        if eachConfigProfileDetails.get('expireAfter') == None:
            eachConfigProfileDetails['expireAfter'] = self.defaultExpireAfter
        if eachConfigProfileDetails.get('OTPLength') == None:
            eachConfigProfileDetails['OTPLength'] = self.defaultOTPLength
        return eachConfigProfileDetails

        
    def _getConfigBasedOnOTPUsage(self, OTPConfigName):
        if OTPConfigName in self.configProfiles:
            return self.configProfiles[OTPConfigName]
        else:
            raise Exception('No configuration exists with this OTPUsage.')