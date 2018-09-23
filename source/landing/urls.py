from django.conf.urls import url
from .views import contact

urlpatterns = [
    url(r'^contact/$', contact, name="contact"),
]
