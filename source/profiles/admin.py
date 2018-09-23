from django.contrib import admin
from .forms import ProfileForm
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "telefone", "cidade", "profilePic"]
    form = ProfileForm
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)
