from allauth.account.adapter import DefaultAccountAdapter
from django.http import Http404
from django.contrib.auth import get_user_model
import time

User = get_user_model()

class NoSignupAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False  # Esto desactiva completamente el registro

    def respond_user_inactive(self, request, user):
        raise Http404  # Opcional: evita mostrar página de usuario inactivo
    
    def send_mail(self, template_prefix, email, context):
        if User.objects.filter(email=email).exists():
            super().send_mail(template_prefix, email, context)
        else:
            time.sleep(3)