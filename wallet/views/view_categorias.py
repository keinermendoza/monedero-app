from django import forms
from django.urls import reverse_lazy
from .mixins import (
    RequireSuperUser,
    HtmxListFormView,
    HtmxEditUpdateDeleteView
)
from wallet.models import (
    CategoriaMovimiento
)

class CategoriaMovimientoForm(forms.ModelForm):
    class Meta: 
        model = CategoriaMovimiento
        fields = "__all__"

class CategoriaMovimientoView(RequireSuperUser, HtmxListFormView):
    template_name = "wallet/categoria_movimiento/index.html"
    template_partial_name = "cotton/ui/categoria_movimiento/partial_table.html"
    template_form_partial_name = "cotton/ui/form.html"
    paginate_by = 20
    queryset = CategoriaMovimiento.objects.all()
    form_class = CategoriaMovimientoForm
    context_object_name = "categorias"
    retry_url = reverse_lazy("categoria_listar_registrar")
    success_url = reverse_lazy("categoria_listar_registrar")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "modal_detail_id":"movimiento_detail",
            "modal_detail_container_id":"movimiento_detail_modal_container",
        })
        return context

from django.contrib import messages 

class CategoriaMovimientoEditDeleteView(RequireSuperUser, HtmxEditUpdateDeleteView):
    template_name = "cotton/ui/form.html"
    form_class = CategoriaMovimientoForm
    success_url = reverse_lazy("categoria_listar_registrar")
    queryset = CategoriaMovimiento.objects.all()

    def display_error_delete_message(self):
        messages.error(self.request, "No es posible eliminar esta categoria hasta eliminar todos los movimientos que la usan")
    
    def display_success_delete_message(self):
        messages.success(self.request, "Categoria eliminada con exito")

    def get_retry_url(self):
        return reverse_lazy("categoria_editar_eliminar", args=[self.kwargs['pk']])

  
    