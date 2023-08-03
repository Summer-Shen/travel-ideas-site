from django.contrib import admin

from ti.models import User, Idea, Tag, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")


class IdeaAdmin(admin.ModelAdmin):
    list_display = ("user_id", "title", "destination", "start_date", "end_date", "created_at", "modified_at")


class TagAdmin(admin.ModelAdmin):
    list_display = ("idea_id", "name")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("idea_id", "user_id", "content", "created_at")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
