from django.core.validators import RegexValidator

phone_regex = RegexValidator(
        regex=r'\d{10}',
        message="Your phone number appears to be invalid. Please double-check it"
    )