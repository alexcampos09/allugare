import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm
from .models import Profile

@login_required
def profile_detail(request, username=None):
    obj = get_object_or_404(User, username=username)
    user = obj.profile

    # SOCIAL ACCOUNT
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
        print(plus_token)
        fb_picture = r.json()['picture']['data']['url']
        fb_name = r.json()['name']
    except:
        fb_picture = None
        fb_name = None

    context = {
        "object": obj,
        "user": user,
        "fb_picture": fb_picture,
        "fb_name": fb_name
    }
    template = 'profile_detail.html'
    return render(request, template, context)

@login_required
def profile_update(request, username=None):
    obj = get_object_or_404(User, username=username)
    user = obj.profile
    form = ProfileForm(request.POST or None, request.FILES or None, instance = user)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/profiles/{username}'.format(username=user.user))
    template = 'profile_update.html'
    return render(request, template, context)
