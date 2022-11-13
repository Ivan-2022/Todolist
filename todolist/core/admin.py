from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fields_list = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_fields = ('is_staff', 'is_active', 'is_superuser')
    exclude = ('password',)
    readonly_fields = ('last_login', 'date_joined')
