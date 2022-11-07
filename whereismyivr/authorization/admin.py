from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    # Inline для отображения профиля пользователя в таблице Пользователи
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    # настройка отображения модели пользователя в панели администратора
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_superuser", "is_active")
    ordering = ("date_joined",)


class ProfileAdmin(admin.ModelAdmin):
    # настройка отображения модели профиля пользователя в панели администратора
    list_display = ('user', 'profile_pic', 'profile_type', 'telegram_username', 'vk_username')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
