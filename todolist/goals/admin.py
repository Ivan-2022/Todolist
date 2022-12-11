from django.contrib import admin

from .models import Category, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Category, GoalCategoryAdmin)


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "priority", "created", "updated")
    search_fields = ("title", "user", "description")


admin.site.register(Goal, GoalAdmin)
