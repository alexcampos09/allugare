from django.conf.urls import url
from .views import profile_detail, profile_update

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', profile_detail, name='profile_detail'),
    url(r'^(?P<username>[\w.@+-]+)/update/$', profile_update, name='profile_update'),
]
