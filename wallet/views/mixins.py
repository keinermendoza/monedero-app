from django.contrib.auth.mixins import UserPassesTestMixin
from django_htmx.http import HttpResponseClientRedirect
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    View
)
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin

class RequireSuperUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
class HtmxFormMixing(FormMixin):
    """
    Mixing for handeling htmx form processing
    if valid:
        try to save instance to db (you can avoid this overriding the save method)
        triggers a full client refresh
        optionally you can hook display_success_message for add message to session 

    if invalid:
        return a partial of form with errors
        optionally you can hook display_error_message for add message to session 
    
    requires the implementation of render_to_response as in TemplateResponseMixing
    """
    template_form_partial_name = None

    def call_if_exists(self, method_name):
        method = getattr(self, method_name, None)
        if method is not None and callable(method):
            return method()

    def get_context_form_data(self, **kwargs):
        """Renamed for avoiding collitions 
        Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
            kwargs["endpoint"] = self.get_retry_url()

        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def form_invalid(self, form, **kwrags):
        """If the form is invalid, render the invalid form."""
        self.call_if_exists("display_error_message")
        return self.render_to_response(self.get_context_form_data(**kwrags))
    
    def save(self, form):
        """
        you can override this for adding extra data when saving 
        must return the saved object
        """
        object = form.save()
        return object

    def form_valid(self, form):
        self.object = self.save(form)
        self.call_if_exists("display_success_message")
        return HttpResponseClientRedirect(self.get_success_url())
    
    def get_retry_url(self):
        if self.retry_url is not None:
            return self.retry_url
        raise NotImplementedError('for use HtmxViewMixing you must to provide a retry_url property or implement get_retry_url method')

        
class HtmxEditUpdateDeleteView(View, TemplateResponseMixin, HtmxFormMixing, SingleObjectMixin):
    template_name = None
    extra_context = {
        "btn_text":"Guardar Cámbios"
    }

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object"):
            kwargs.update({
                "instance": self.object
            })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_form = self.get_context_form_data()
        context.update(**context_form)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            self.call_if_exists("display_success_delete_message")
        except Exception as e:
            self.call_if_exists("display_error_delete_message")
            
        return HttpResponseClientRedirect(success_url)  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())
   
class HtmxListFormView(ListView, HtmxFormMixing):
    """
    Handles List/Create cicle using a combination of traditional http and htmx request/responses   
    GET: renders full page (template_name) and also partial template (template_partial_name) if recives htmx requests
    POST: accepts htmx form and triggers full reload if success else return form with errors
    """
    template_name = None
    template_partial_name = None
    template_form_partial_name = None
    extra_context = {
        "btn_text":"Registrar"
    }

    def get_template_names(self) -> list[str]:
        if self.request.method == "POST":
            return [self.template_form_partial_name]
        if self.request.htmx:
            return [self.template_partial_name]
        return [self.template_name]
   
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_form = self.get_context_form_data()
        context.update(**context_form)
        return context