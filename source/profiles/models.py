from django.conf import settings
# from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import smart_text

UF_CHOICES = (
    ('SP', 'SP'), ('AC', 'AC'), ('AL', 'AL'), ('AM', 'AM'), ('AP', 'AP'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
    ('GO', 'GO'), ('MA', 'MA'), ('MG', 'MG'), ('MS', 'MS'), ('MT', 'MT'), ('PA', 'PA'), ('PB', 'PB'), ('PE', 'PE'),
    ('PI', 'PI'), ('PR', 'PR'), ('RJ', 'RJ'), ('RO', 'RO'), ('RN', 'RN'), ('RR', 'RR'), ('RS', 'RS'), ('SC', 'SC'),
    ('SE', 'SE'), ('TO', 'TO'),
)

User = settings.AUTH_USER_MODEL # 'auth.User'

def upload_location(instance, filename):
    return "%s/Profile/%s" %(instance.user, filename)

class Profile(models.Model):
    user        = models.OneToOneField(User)
    id          = models.AutoField(primary_key=True)
    width       = models.IntegerField(default=0, null=True, blank=True,)
    height      = models.IntegerField(default=0, null=True, blank=True,)
    profilePic  = models.ImageField(
                    upload_to = upload_location,
                    blank=True, null=True,
                    verbose_name = 'Foto de Perfil',
                    width_field="width",
                    height_field="height",
                    )
    nome        = models.CharField(max_length = 120, blank = True, null=True, verbose_name = 'Nome completo')
    universidade= models.CharField(max_length = 120, blank=True, null=True)
    curso       = models.CharField(max_length = 120, blank=True, null=True)
    uf          = models.CharField(max_length = 2, blank=True, null=True, choices = UF_CHOICES, verbose_name = 'UF')
    cidade      = models.CharField(max_length=120, null=True, blank=True)
    telefone    = models.CharField(max_length = 20, blank=True, null=True, verbose_name = 'Telefone para Contato', help_text = "Essa informação não estará visível para outros usuários.")
    bio         = models.TextField(
                    blank=True,
                    null=True,
                    verbose_name = 'Biografia',
                    help_text = "Quem é você e com quem gostaria de morar?",
                    )


    def __str__(self):
        return smart_text(self.user.username)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=User)
