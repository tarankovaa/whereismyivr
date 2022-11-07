from PIL import Image
from django.db import models
from django.contrib.auth.models import User

from .validators import alphanumeric_underscore


class Profile(models.Model):
    # модель профиля пользователя
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
        # настройки модели
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        # строковое представление объекта профиля - имя пользователя
        return self.user.username

    def save(self, *args, **kwargs):
        # обрезка фотографии профиля пользователя под квадрат
        super().save()
        img = Image.open(self.profile_pic)

        img = img.crop(((img.width - min(img.size)) // 2,
                        (img.height - min(img.size)) // 2,
                        (img.width + min(img.size)) // 2,
                        (img.height + min(img.size)) // 2))

        img.save(self.profile_pic.path)

    def is_customer(self):
        # возвращает, является ли пользователь заказчиком
        return self.profile_type == self.CUSTOMER

    def is_consultant(self):
        # возвращает, является ли пользователь консультантом
        return self.profile_type == self.CONSULTANT

    def is_performer(self):
        # возвращает, является ли пользователь исполнителем
        return self.profile_type == self.PERFORMER
