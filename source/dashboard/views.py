import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin, TemplateView, TemplateResponseMixin

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class MyView(LoginRequiredMixin, ContextMixin, TemplateResponseMixin, View):
    def get(self, request, *args, **kwargs):
        # Class Based Views in Login Required Decorator & Custom Mixin
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
