from crispy_forms.bootstrap import InlineField, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Div, Field
# from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from django import forms
from .models import Imovel, ImovelPhotos

UF_CHOICES = (
    ('SP', 'SP'), ('AC', 'AC'), ('AL', 'AL'), ('AM', 'AM'), ('AP', 'AP'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'),
    ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MG', 'MG'), ('MS', 'MS'), ('MT', 'MT'), ('PA', 'PA'), ('PB', 'PB'),
    ('PE', 'PE'), ('PI', 'PI'), ('PR', 'PR'), ('RJ', 'RJ'), ('RO', 'RO'), ('RN', 'RN'), ('RR', 'RR'), ('RS', 'RS'),
    ('SC', 'SC'), ('SE', 'SE'), ('TO', 'TO'),
)

TIPO_IMOVEL_CHOICES = (
    ('Casa', 'Casa'),
    ('Apartamento', 'Apartamento'),
    ('Kitnet', 'Kitnet'),
    ('Edicula', 'Edícula'),
    ('Outro', 'Outro'),
)

INT_CHOICES = [tuple([x,x]) for x in range(0, 11)]

class ImovelForm(forms.ModelForm):
    uf              = forms.CharField(label = 'Estado', widget=forms.Select(choices = UF_CHOICES))
    tipo_imovel     = forms.CharField(widget=forms.Select(choices = TIPO_IMOVEL_CHOICES))
    qtd_quartos     = forms.IntegerField(label = 'Quartos', widget=forms.Select(choices = INT_CHOICES))
    qtd_banheiros   = forms.IntegerField(label= 'Banheiros', widget=forms.Select(choices = INT_CHOICES))
    qtd_vagas       = forms.IntegerField(label = 'Vagas de Garagem', widget=forms.Select(choices = INT_CHOICES))
    move_in_date    = forms.DateField(label = 'Vago a partir de: ', widget=forms.SelectDateWidget)

    # visita_fotografica = forms.DateTimeField(label = 'Agendar visita fotográfica: ', widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    # visita_fotografica = forms.DateTimeField(label = 'Agendar visita fotográfica: ', required=False)

    class Meta:
        model = Imovel
        fields = [
            "uf",
            "cidade",
            "bairro",
            "rua",
            "numero",
            "complemento",
            "cep",
            "referencia",
            "tipo_imovel",
            "area_util",
            "qtd_quartos",
            "qtd_banheiros",
            "qtd_vagas",
            "mobiliado",
            "descricao",
            "preco_locacao",
            "preco_condominio",
            "iptu",
            "conta_agua",
            "conta_luz",
            "move_in_date",
            "active",
            # "visita_fotografica",
            "video"
        ]
        widgets = {
            'numero': forms.TextInput,
            'preco_locacao': forms.TextInput,
            'preco_condominio': forms.TextInput,
            'iptu': forms.TextInput,
            "move_in_date": forms.TextInput(attrs={'type': 'date'})
        }



    def __init__(self, *args, **kwargs):
        super(ImovelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_id = 'id-ImovelForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        # self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Enviar'))


        self.helper.layout = Layout(
            Fieldset(
                "Cadastre seu imóvel, {{ user.profile.nome }}!",
                Div(
                    Div('uf',css_class='col-md-6'),
                    Div('cidade',css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('rua',css_class='col-md-6'),
                    Div('numero',css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('complemento',css_class='col-md-6'),
                    Div('cep',css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('bairro',css_class='col-md-6'),
                    Div('referencia',css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('tipo_imovel',css_class='col-md-6'),
                    Div('area_util',css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('qtd_quartos',css_class='col-md-4'),
                    Div('qtd_banheiros',css_class='col-md-4'),
                    Div('qtd_vagas',css_class='col-md-4'),
                    css_class='row',
                ),
                # HTML("""<p>We use notes to get better, <strong>please help us</strong></p>"""),
                "descricao",
                Div(
                    Div(PrependedText('preco_locacao', 'R$'),css_class='col-md-6'),
                    Div(PrependedText('preco_condominio', 'R$'),css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div(PrependedText('iptu', 'R$'),css_class='col-md-4'),
                    Div(PrependedText('conta_agua', 'R$'),css_class='col-md-4'),
                    Div(PrependedText('conta_luz', 'R$'),css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    Div('move_in_date',css_class='col-md-3', id='date'),
                    Div('mobiliado',css_class='col-md-4'),
                    Div('active',css_class='col-md-4'),
                    css_class='row',
                ),
                Div(
                    # Div('visita_fotografica',css_class='col-md-4', id='date'),
                    Div('video',css_class='col-md-8'),
                    css_class='row',
                ),
            ),
            # ButtonHolder(
            #     Submit('submit', 'Enviar', css_class='button white')
            # )
        )



class ImovelPhotosForm(forms.ModelForm):

    class Meta:
        model = ImovelPhotos
        fields = [
            "photos",
            # "order"
        ]
