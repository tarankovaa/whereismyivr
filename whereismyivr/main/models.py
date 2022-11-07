from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    # модель заявки
    RESEARCH = "RE"
    PROJECT = "PR"
    TYPE_OF_APP_CHOICES = (
        (RESEARCH, "Исследование"),
        (PROJECT, "Проект"),
    )
    TYPE_OF_FIELD_CHOICES = (
        ("it", "IT"),
        ("business", "Бизнес"),
        ("design", "Дизайн"),
        ("publishing", "Издательское дело"),
        ("engineering", "Инженерия"),
        ("media", "Медиа"),
        ("education", "Образование"),
        ("events", "Организация событий"),
        ("oriental_studies", "Востоковедение"),
        ("natural_sciences", "Естественные науки"),
        ("art", "Искусствоведение"),
        ("history", "История"),
        ("culturology", "Культурология"),
        ("marketing", "Маркетинг"),
        ("maths", "Математика"),
        ("management", "Менеджмент"),
        ("linguistics", "Лингвистика"),
        ("politics", "Политология"),
        ("right", "Право"),
        ("psychology", "Психология"),
        ("sociology", "Социология"),
        ("philology", "Филология"),
        ("philosophy", "Философия"),
        ("economy", "Экономика"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.TextField("Название", blank=False)
    type_of_card = models.CharField(
        "Исследование или проект",
        max_length=2,
        choices=TYPE_OF_APP_CHOICES,
        blank=False
    )
    field_of_card = models.CharField(
        "Область",
        max_length=20,
        choices=TYPE_OF_FIELD_CHOICES,
        blank=False
    )

    customer = models.BooleanField("Заказчик", default=False)
    consultant = models.BooleanField("Консультант", default=False)
    performer = models.BooleanField("Исполнитель", default=False)
    partner = models.BooleanField("Напарник", default=False)

    product_image = models.TextField("Образ продукта", blank=False)
    created_on = models.DateTimeField("Дата создания", default=datetime.now)

    class Meta:
        # настройка модели (отображаемое имя)
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        # возвращает строковое представление объекта заявки - название
        return self.title

    def get_type_of_card(self):
        # возвращает тип заявки - проект или исследование
        if self.type_of_card == self.RESEARCH:
            return "Исследование"
        return "Проект"

    def get_field_of_card(self):
        # возвращает область проекта или исследования
        for field in self.TYPE_OF_FIELD_CHOICES:
            if field[0] == self.field_of_card:
                return field[1]

    def get_search_for(self):
        # возвращает разыскиваемые должности
        search_for = []
        if self.customer:
            search_for.append("Заказчик")
        if self.consultant:
            search_for.append("Консультант")
        if self.performer:
            search_for.append("Исполнитель")
        if self.partner:
            search_for.append("Напарник")
        return search_for
