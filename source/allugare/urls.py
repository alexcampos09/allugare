"""allugare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from dashboard.views import MyView


urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^accounts/', include('allauth.urls')),
    # my Apps URLs
    url(r'^profiles/', include('profiles.urls'), name="profiles"),
    url(r'^lares/', include('lares.urls'), name="lares"),
    url(r'^land/', include('landing.urls'), name="land"),
    url(r'^mensagens/', include('mensagens.urls'), name="mensagens"),
    # URLs
    # url(r'^geocoder$', TemplateView.as_view(template_name='geocoder.html'), name="geocoder"),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"), # use {% url 'url_name' %} instead of hardcoding it
    url(r'^sobre$', TemplateView.as_view(template_name='sobre.html'), name="sobre"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
