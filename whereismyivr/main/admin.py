from django.contrib import admin
from .models import Card


class CardAdmin(admin.ModelAdmin):
    # настройка отображения заявки в панели администратора
    list_display = ("user", "title", "product_image", "customer", "consultant", "performer", "partner")
    list_filter = ("customer", "consultant", "performer", "partner")
    search_fields = ("title",)


admin.site.register(Card, CardAdmin)
