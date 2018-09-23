import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import render

from dashboard.views import LoginRequiredMixin
from .forms import MessageForm, ContactForm
from .models import Message


class MessageDetail(DetailView):
    model = Message

    def get_context_data(self, *args, **kwargs):

        # SOCIAL ACCOUNT
        user = self.object.user.profile
        try:
            # FOR LOOPING
            # fball = SocialAccount.objects.filter(
            #         provider = 'facebook')
            fbid = SocialAccount.objects.filter(
                    user = user.user,
                    provider = 'facebook').first()
            social_token = SocialToken.objects.filter(
                    account__user = user.user,
                    account__provider = 'facebook').first()
            uid = fbid.uid
            token = social_token.token
            base_url = "https://graph.facebook.com/v2.5/"
            basic_info = "{base_url}{fb_uid}?fields=id,name,picture.type(large)&format=json".format(
                        base_url=base_url,
                        fb_uid = uid)
            plus_token = "{basic_info}&access_token={token}".format(
                        basic_info=basic_info,
                        token=token)
            r = requests.get(plus_token)
            # print(r.status_code, uid, token, r.text, r.json())
            fb_picture = r.json()['picture']['data']['url']
            fb_name = r.json()['name']
        except:
            fb_picture = None
            fb_name = None

        context = super(MessageDetail, self).get_context_data(**kwargs)
        context.update({"fb_picture": fb_picture, "fb_name": fb_name })
        return context

class MessageList(ListView):
    model = Message
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(MessageList, self).get_queryset(*args, **kwargs).order_by("-updates")
        return qs

class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = "/mensagens/"

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
        return super(MessageCreate, self).form_valid(form)

class MessageUpdate(LoginRequiredMixin, UpdateView):
    # SECURITY ISSUE, ANYONE LOGGED IN CAN EDIT ANY MESSAGE OR PROPERTY (LARES) IF THEY WRITE '/UPDATE' AFTER AN USER ADDED POST
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = "/mensagens/"

class MessageDelete(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "message_delete.html"
    success_url = "/mensagens/"



def contato(request):
    title = 'Entre em contato por e-mail ou telefone'
    form = ContactForm(request.POST or None)
    context = {
        "form": form,
        "title": title
    }
    if form.is_valid():
        form_name = form.cleaned_data.get('nome')
        form_message = form.cleaned_data.get('mensagem')
        form_email = form.cleaned_data.get('email')
        # print (name, mensagem, email)
        subject = 'Contato do site'
        contact_message = '''
            %s enviou a seguinte mensagem para Allugare através do e-mail %s:

            "%s"

            Agradecemos a sua mensagem e entraremos em contato em breve.

            Atenciosamente,
            Allugare
            ''' %(
                form_name,
                form_email,
                form_message,
            )
        context = {
            "title": "Obrigado!"
        }
        from_email = settings.EMAIL_HOST_USER
        to_email = [form_email, from_email]

        send_mail(
            subject,
            contact_message,
            from_email,
            to_email,
            fail_silently = False
        )
    return render(request, 'contato.html', context)
