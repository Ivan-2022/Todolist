from django.contrib import admin

from .models import Category, Goal, Board, Comment, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Category, GoalCategoryAdmin)


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "status", "priority", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Goal, GoalAdmin)


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'goal', 'created', 'updated')
    search_fields = ('text', 'user')


admin.site.register(Comment, GoalCommentAdmin)


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


admin.site.register(Board, BoardAdmin)


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role')
    search_fields = ('board', 'user', 'role')


admin.site.register(BoardParticipant, BoardParticipantAdmin)
