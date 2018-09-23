from django.contrib import admin
from .models import Message
from .forms import MessageForm

class MessageAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        "__str__",
        "mensagem",
        "timestamp",
        ]
        
    form = MessageForm
    class Meta:
        model = Message

admin.site.register(Message, MessageAdmin)
