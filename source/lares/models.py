from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.forms import ModelForm, Textarea
from django.utils import timezone
from django.utils.encoding import smart_text

User = settings.AUTH_USER_MODEL # 'auth.User'

def upload_location(instance, filename):
    return "%s/%s/%s" %(instance.user, instance, filename)

class Imovel(models.Model):
    # usuário
    user    = models.ForeignKey(User)
    id      = models.AutoField(primary_key=True)
    active  = models.BooleanField(default = True, verbose_name = "Anúncio Ativo")
    # endereço
    uf              = models.CharField(max_length = 2, blank=False, verbose_name = 'Estado')
    cidade          = models.CharField(max_length = 120, blank=False)
    bairro          = models.CharField(max_length = 120, blank=False)
    rua             = models.CharField(max_length = 120, blank=False, verbose_name= 'Rua, avenida, alameda')
    numero          = models.PositiveIntegerField(blank=False, verbose_name = 'Número')
    complemento     = models.CharField(max_length = 120, blank=True, null=True)
    cep             = models.CharField(max_length = 10, blank=False, verbose_name = 'CEP')
    referencia      = models.CharField(max_length = 120, blank = True, null = True, verbose_name="Referência")
    # características do imóvel
    tipo_imovel     = models.CharField(max_length = 20, blank=False, verbose_name = 'Tipo de Imóvel', default = 'Casa')
    area_util       = models.PositiveIntegerField(blank=True, null=True, verbose_name ='Área Útil (m²)')
    qtd_quartos     = models.PositiveIntegerField(verbose_name = 'Quantidade de Quartos')
    qtd_banheiros   = models.PositiveIntegerField(verbose_name = 'Quantidade de Banheiros')
    qtd_vagas       = models.PositiveIntegerField(blank=True, null=True, verbose_name = 'Vagas de Garagem')
    mobiliado       = models.BooleanField(default = False)
    descricao       = models.TextField(
                        blank=True,
                        null=True,
                        verbose_name = 'Descrição do Imóvel',
                        help_text = "Mobiliado, piscina, quintal, área externa, etc.",
                    )
    # preço
    preco_locacao   = models.DecimalField(max_digits = 8, decimal_places = 2, blank=False, verbose_name = 'Aluguel')
    preco_condominio= models.DecimalField(max_digits = 8, decimal_places = 2, blank=False, verbose_name = 'Condomínio (se houver)', default = 0)
    iptu            = models.DecimalField(max_digits = 8, decimal_places = 2, blank=False, verbose_name = 'IPTU', default = 0)
    conta_agua      = models.DecimalField(max_digits = 8, decimal_places = 2, blank=False, verbose_name = 'Conta de água', default = 0)
    conta_luz       = models.DecimalField(max_digits = 8, decimal_places = 2, blank=False, verbose_name = 'Conta de luz', default = 0)
    def _get_total_price(self):
        # return round(self.preco_locacao + self.preco_condominio + self.conta_agua + self.conta_luz + self.iptu/12, 0)
        return round(self.preco_locacao + self.preco_condominio + self.iptu/12, 0)
    preco_total     = property(_get_total_price)

    # data mudança
    move_in_date = models.DateField(auto_now_add = False, auto_now = False, default = timezone.now)
    # timestamp
    timestamp   = models.DateField(auto_now_add = True, auto_now = False)
    updates     = models.DateTimeField(auto_now_add = False, auto_now = True)

    # agendar visita fotográfica
    # visita_fotografica = models.DateTimeField(auto_now_add = False, auto_now = False, blank=True, null=True)

    # URL de Vídeo
    video = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return smart_text(self.bairro)

    def get_absolute_url(self):
        return reverse("imovel_detail", kwargs={"pk":self.pk})

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"
        ordering = ["-timestamp", "-updates"]

class ImovelPhotos(models.Model):
    user    = models.ForeignKey(User)
    imovel  = models.ForeignKey(Imovel)
    order = models.PositiveIntegerField(default=0, null=True, blank=True)
    # order   = models.PositiveIntegerField(blank = True, null = True)
    width   = models.IntegerField(default=0, null=True, blank=True,)
    height  = models.IntegerField(default=0, null=True, blank=True,)
    photos  = models.ImageField(
                upload_to = upload_location,
                blank=False,
                verbose_name = 'Fotos',
                width_field="width",
                height_field="height",
                )

    def __str__(self):
        return self.imovel.bairro

    class Meta:
        ordering = ('order',)

















    #
