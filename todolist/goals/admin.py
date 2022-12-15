from django.contrib import admin

from .models import Category, Goal, Board


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user", "board")


admin.site.register(Category, GoalCategoryAdmin)
admin.site.register(Board)


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "priority", "created", "updated")
    search_fields = ("title", "user", "description")


admin.site.register(Goal, GoalAdmin)
