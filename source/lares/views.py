import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.core.urlresolvers import reverse_lazy
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from dashboard.views import LoginRequiredMixin

from .forms import ImovelForm, ImovelPhotosForm
from .models import Imovel, ImovelPhotos

class ImovelDetail(DetailView):
    model = Imovel

    def get_context_data(self, *args, **kwargs):
        address = (self.object.rua, self.object.numero, self.object.bairro, self.object.cep, self.object.cidade, self.object.uf)
        api_key = "AIzaSyAiw0iU0egdeVrOKboOOZ2n1WXS3Os0WgI"
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()

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


        if api_response_dict['status'] == 'OK':
            context = super(ImovelDetail, self).get_context_data(**kwargs)
            lat = api_response_dict['results'][0]['geometry']['location']['lat']
            lng  = api_response_dict['results'][0]['geometry']['location']['lng']
            latitude = str(lat)
            longitude = str(lng)
            context.update({'latitude': latitude, 'longitude': longitude, 'fb_picture': fb_picture, "fb_name": fb_name})
            return context

        else:
            context = super(ImovelDetail, self).get_context_data(**kwargs)
            context.update({"fb_picture": fb_picture, "fb_name": fb_name})
            return context


class ImovelList(ListView):
    model = Imovel
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super(ImovelList, self).get_queryset(*args, **kwargs).order_by("-updates")
        return qs

class ImovelCreate(LoginRequiredMixin, CreateView):
    model = Imovel
    form_class = ImovelForm
    template_name = "imovel_create.html"
    # success_url = "/lares/"

    def get_success_url(self):
        return reverse('imovel_detail', kwargs={'pk' : self.object.pk})
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ImovelCreate, self).get_form_kwargs(*args, **kwargs)
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
        return super(ImovelCreate, self).form_valid(form)

class ImovelUpdate(LoginRequiredMixin, UpdateView):
    model = Imovel
    form_class = ImovelForm
    template_name = "imovel_create.html"
    # success_url = "/lares/"

    def get_absolute_url(self):
        return reverse('imovel_create', kwargs={"pk":self.pk})
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ImovelUpdate, self).get_form_kwargs(*args, **kwargs)
        return kwargs

class ImovelDelete(LoginRequiredMixin, DeleteView):
    model = Imovel
    template_name = "imovel_delete.html"
    success_url = "/lares/"

def photos_formset(request, *args, **kwargs):
    pk = kwargs['pk']
    ImovelPhotosModelFormset = modelformset_factory(ImovelPhotos, form=ImovelPhotosForm, can_delete=True, can_order=True)
    formset = ImovelPhotosModelFormset(
            request.POST or None, request.FILES or None,
            queryset = Imovel.objects.get(pk=pk).imovelphotos_set.all(),
        )
    if formset.is_valid():
        instance = formset.save(commit=False)
        if request.FILES:
            for form in formset:
                if form.is_valid():
                    if form.cleaned_data != {}:
                        obj = form.save(commit=False)
                        obj.user = request.user
                        obj.imovel = Imovel.objects.get(pk=pk)
                        obj.order = form.cleaned_data['ORDER']
                        obj.save()
        for img in formset.deleted_objects:
            print ("deleted image")
            img.delete()
        return HttpResponseRedirect('/lares/{pk}/'.format(pk=pk))

    context = {
        "formset": formset,
    }
    return render(request, "imovel_photos.html", context)

# DOES THE SAME THING AS THE photos_formset FUNCTION ABOVE, BUT NOT THAT WELL
# class ImovelPhotosView(LoginRequiredMixin, CreateView):
#     model = Imovel
#     form_class = ImovelPhotosForm
#     template_name = "imovel_photos.html"
#     success_url = "/lares/"
#
#     def form_valid(self, form):
#         pk = self.kwargs['pk']
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = self.request.user
#             obj.imovel = Imovel.objects.get(pk=pk)
#             obj.save()
#         return super(ImovelPhotosView, self).form_valid(form)
