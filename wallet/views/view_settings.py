from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from django.views.generic import (
    ListView,
    DetailView,
    View,
    CreateView,
    UpdateView,
    TemplateView
)
from django.views.generic.detail import SingleObjectMixin
from django_htmx.http import HttpResponseClientRedirect
from django.views.generic.edit import ProcessFormView

from .mixins import (
    RequireSuperUser
)

from wallet.models import (
    Movimiento
)

class SettingsView(TemplateView):
    template_name = "wallet/home.html"
    
