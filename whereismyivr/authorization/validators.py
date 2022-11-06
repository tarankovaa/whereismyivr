from django.core.validators import RegexValidator

alphanumeric_underscore = RegexValidator(r'^[_0-9a-zA-Z]{5,}$',
                                         'Only alphanumeric characters and underscores are allowed.')
