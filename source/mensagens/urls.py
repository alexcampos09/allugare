from django.conf.urls import url
from .views import contato
from .views import MessageDetail, MessageList, MessageCreate, MessageUpdate, MessageDelete

urlpatterns = [
    url(r'^contato/$', contato, name="contato"),
    url(r'^$', MessageList.as_view(), name="message_list"),
    url(r'^create/$', MessageCreate.as_view(), name="message_create"),
    url(r'^(?P<pk>\d+)/$', MessageDetail.as_view(), name="message_detail"),
    url(r'^(?P<pk>\d+)/update/$', MessageUpdate.as_view(), name="message_update"),
    url(r'^(?P<pk>\d+)/delete/$', MessageDelete.as_view(), name="message_delete"),
]
