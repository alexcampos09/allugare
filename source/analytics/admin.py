from django.contrib import admin

from .models import UserSession

class UserSessionAdmin(admin.ModelAdmin):

    def email(self, instance):
        return instance.user.email

    list_display = [
        "__str__",
        "user",
        "email",
        "timestamp",
        ]

    class Meta:
        model = UserSession

admin.site.register(UserSession, UserSessionAdmin)
