from django.core.validators import RegexValidator
import re


ASCIIUsernameValidator = RegexValidator(regex=r"^[\w.]+\Z",
                                            message=("Enter a valid username. This value may contain only English letters, "
                                                    "numbers, and @/./+/-/_ characters."),
                                            flags=re.ASCII)