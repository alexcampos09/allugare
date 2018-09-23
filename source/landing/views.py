from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LandingPageForm

def contact(request):
    title = 'Quero sugestões de imóveis!'
    form = LandingPageForm(request.POST or None)
    context = {
        "form": form,
        "title": title,
    }

    if form.is_valid():
        obj = form.save(commit=False)
        # obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect('/')

    return render(request, 'contact.html', context)
