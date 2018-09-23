from django.conf import settings
from django.core.urlresolvers import reverse
# from django.core.validators import RegexValidator
from django.db import models
# from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL # 'auth.User'

class Message(models.Model):
    user        = models.ForeignKey(User)
    id          = models.AutoField(primary_key=True)
    anuncio     = models.CharField(max_length = 140, blank=False, null=False, verbose_name="Anúncio", unique=True)
    mensagem    = models.TextField(max_length = 5000, blank=False)
    timestamp   = models.DateField(auto_now_add = True, auto_now = False)
    updates     = models.DateTimeField(auto_now_add = False, auto_now = True)

    def __str__(self):
        return self.anuncio

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk":self.pk})

    class Meta:
        verbose_name = "Anúncio"
        verbose_name_plural = "Anúncios"
        ordering = ["-timestamp", "-updates"]
