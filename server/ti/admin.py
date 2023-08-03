from django.contrib import admin

from ti.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')


# Register your models here.
admin.site.register(User, UserAdmin)
