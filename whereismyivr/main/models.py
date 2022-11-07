from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    # модель заявки
    RESEARCH = "RE"
    PROJECT = "PR"
    TYPE_OF_FIELD_CHOICES = (
        ("it_project", "IT — проект"),
        ("business_project", "Бизнес — проект"),
        ("design", "Дизайн — проект"),
        ("publishing", "Издательское дело — проект"),
        ("engineering", "Инженерия — проект"),
        ("media", "Медиа — проект"),
        ("education_project", "Образование — проект"),
        ("events", "Организация событий — проект"),
        ("it_research", "IT — исследование"),
        ("business_research", "Бизнес — исследование"),
        ("oriental_studies", "Востоковедение — исследование"),
        ("natural_sciences", "Естественные науки — исследование"),
        ("art", "Искусствоведение — исследование"),
        ("history", "История — исследование"),
        ("culturology", "Культурология — исследование"),
        ("marketing", "Маркетинг — исследование"),
        ("maths", "Математика — исследование"),
        ("management", "Менеджмент — исследование"),
        ("linguistics", "Лингвистика — исследование"),
        ("education_research", "Образование — исследование"),
        ("politics", "Политология — исследование"),
        ("right", "Право — исследование"),
        ("psychology", "Психология — исследование"),
        ("sociology", "Социология — исследование"),
        ("philology", "Филология — исследование"),
        ("philosophy", "Философия — исследование"),
        ("economy", "Экономика — исследование"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.TextField("Название", blank=False)

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
        for field in self.TYPE_OF_FIELD_CHOICES:
            if field[0] == self.field_of_card:
                return field[1].split(" — ")[1].capitalize()

    def get_field_of_card(self):
        # возвращает область проекта или исследования
        for field in self.TYPE_OF_FIELD_CHOICES:
            if field[0] == self.field_of_card:
                return field[1].split(" — ")[0]

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
