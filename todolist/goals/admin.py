from django.contrib import admin

from .models import Category


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Category, GoalCategoryAdmin)
