from django.core.validators import RegexValidator


PhoneNumberValidator = RegexValidator(regex= r"09(0[0-3]|1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}",
                                      message= "Invalid phone number. Please enter a phone number with correct format.",
                                    )