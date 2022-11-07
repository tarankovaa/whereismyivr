from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from .validators import alphanumeric_underscore


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    CUSTOMER = "CU"
    CONSULTANT = "CO"
    PERFORMER = "PE"
    PROFILE_TYPE_CHOICES = [
        (PERFORMER, "Исполнитель"),
        (CUSTOMER, "Заказчик"),
        (CONSULTANT, "Консультант"),
    ]

    profile_pic = models.ImageField(
        "Фото профиля",
        default='default.jpg',
        upload_to='profile_images')

    profile_type = models.CharField(
        "Тип профиля",
        max_length=2,
        blank=False,
        default=PERFORMER,
        choices=PROFILE_TYPE_CHOICES)

    telegram_username = models.CharField(
        "Имя пользователя в Telegram",
        max_length=32,
        blank=True,
        validators=[alphanumeric_underscore])

    vk_username = models.CharField(
        "Имя пользователя в VK",
        max_length=32,
        blank=True,
        validators=[alphanumeric_underscore])

    is_filled = models.BooleanField("Заполнен", default=False)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.profile_pic.path)

    '''def get_email(self):
        return self.user.email

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name'''

    def is_customer(self):
        return self.profile_type == self.CUSTOMER

    def is_consultant(self):
        return self.profile_type == self.CONSULTANT

    def is_performer(self):
        return self.profile_type == self.PERFORMER


'''from django.contrib.auth.models import UserProfile as UserAuthModel
from django.db import models


class User(UserAuthModel):
    CUSTOMER = "CU"
    CONSULTANT = "CO"
    PERFORMER = "PE"
    PROFILE_TYPE_CHOICES = [
        (PERFORMER, "Исполнитель"),
        (CUSTOMER, "Заказчик"),
        (CONSULTANT, "Консультант"),
    ]
    profile_pic = models.ImageField("Фото профиля", blank=True)
    profile_type = models.CharField("Тип профиля", max_length=2, blank=True)

    def __str__(self):
        return self.username

    def is_customer(self):
        return self.profile_type == self.CUSTOMER

    def is_consultant(self):
        return self.profile_type == self.CONSULTANT

    def is_performer(self):
        return self.profile_type == self.PERFORMER

'''
