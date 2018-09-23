from django.db import models

class LandingPage(models.Model):
    nome_completo  = models.CharField(max_length=120, blank=False)
    email           = models.EmailField(blank=False)
    telefone        = models.CharField(max_length = 20, blank=True, null=True)
    caracteristicas = models.TextField(
                        max_length = 5000,
                        blank=False,
                        verbose_name = "número de quartos, faixa de preço, etc...",
                        )
    timestamp       = models.DateField(auto_now_add = True, auto_now = False)

    def __str__(self):
        return self.email
