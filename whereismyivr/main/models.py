from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
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
    created_on = models.DateTimeField("Дата создания", default=now)

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        return self.title

    def get_type_of_app(self):
        if self.type_of_card == self.RESEARCH:
            return "Исследование"
        return "Проект"

    def get_search_for(self):
        search_for = []
        if self.customer:
            search_for.append("заказчик")
        if self.consultant:
            search_for.append("консультант")
        if self.performer:
            search_for.append("исполнитель")
        if self.partner:
            search_for.append("напарник")
        search_for[0] = search_for[0].capitalize()
        return "; ".join(search_for)
