from django.core.validators import RegexValidator

# валидатор для Telegram и VK имен пользователей
alphanumeric_underscore = RegexValidator(r'^[_0-9a-zA-Z]{5,}$',
                                         'Только символы латинского алфавита, цифры и нижние подчеркивания разрешены')
