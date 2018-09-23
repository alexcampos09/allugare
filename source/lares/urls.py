from django.conf.urls import include, url
from .views import ImovelDetail, ImovelList, ImovelCreate, ImovelUpdate, ImovelDelete, photos_formset #ImovelPhotosView

urlpatterns = [
    url(r'^$', ImovelList.as_view(), name="imovel_list"),
    url(r'^create/$', ImovelCreate.as_view(), name="imovel_create"),
    url(r'^(?P<pk>\d+)/$', ImovelDetail.as_view(), name="imovel_detail"),
    # url(r'^(?P<pk>\d+)/photos/$', ImovelPhotosView.as_view(), name="imovel_photos"),
    url(r'^(?P<pk>\d+)/photos/$', photos_formset, name="imovel_photos"),
    url(r'^(?P<pk>\d+)/update/$', ImovelUpdate.as_view(), name="imovel_update"),
    url(r'^(?P<pk>\d+)/delete/$', ImovelDelete.as_view(), name="imovel_delete"),
]
