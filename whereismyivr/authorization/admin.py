from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_superuser", "is_active")
    ordering = ("date_joined",)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_pic', 'profile_type', 'telegram_username', 'vk_username')


admin.site.register(Profile, ProfileAdmin)
