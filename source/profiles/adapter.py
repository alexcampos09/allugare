from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/profiles/{username}/"
        return path.format(username=request.user.username)
