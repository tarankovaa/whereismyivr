from django.contrib import admin
from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "type_of_card", "product_image", "customer", "consultant", "performer", "partner")
    list_filter = ("type_of_card", "customer", "consultant", "performer", "partner")
    search_fields = ("title",)


admin.site.register(Card, CardAdmin)
