from django import forms
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum
from django.utils import timezone as tz
from datetime import datetime
from django.urls import reverse_lazy
from .mixins import (
    RequireSuperUser,
    HtmxListFormView,
    HtmxEditUpdateDeleteView
)
from wallet.widgets import CustomDateTimeWidget
from wallet.models import (
    Movimiento,
    CategoriaMovimiento
)

def fecha_valida(fecha_str, formato='%Y-%m-%d'):
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except (ValueError, TypeError):
        return False

class MovimientoForm(forms.ModelForm):
    class Meta: 
        model = Movimiento
        exclude = ["registrado_por"]
        widgets = {
            'fecha': CustomDateTimeWidget(),
        }

class MovimientosView(RequireSuperUser, HtmxListFormView):
    template_name = "wallet/movimientos/index.html"
    template_partial_name = "cotton/ui/movimientos/partial_table.html"
    template_form_partial_name = "cotton/ui/form.html"
    paginate_by = 20
    queryset = Movimiento.objects.all()
    form_class = MovimientoForm
    context_object_name = "movimientos"
    retry_url = reverse_lazy("movimiento_listar_registrar")
    success_url = reverse_lazy("movimiento_listar_registrar")
    
    def save(self, form):
        movimiento = form.save()
        movimiento.registrado_por = self.request.user
        movimiento.save()
        return movimiento
    
    def get_queryset(self):
        queryset = super().get_queryset()
        now = tz.now()
        desde = self.request.GET.get("desde")
        hasta = self.request.GET.get("hasta")

        if all([fecha_valida(desde), fecha_valida(hasta)]):
            queryset = queryset.filter(fecha__gte=desde, fecha__lte=hasta)
            self.filtrando_por_fechas = True
        else:
            queryset = queryset.filter(fecha__year=now.year, fecha__month=now.month)
            self.filtrando_por_fechas = None
        
        if categoria := self.request.GET.get("categoria"):
            return queryset.filter(categoria__nombre=categoria) 
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        gastos =  round(
            queryset.filter(categoria__tipo_movimiento=CategoriaMovimiento.TipoMovimiento.GASTO)
            .aggregate(gastos=Sum("monto"))["gastos"] or 0,
            2
        )        
        ingresos =  round(
            queryset.filter(categoria__tipo_movimiento=CategoriaMovimiento.TipoMovimiento.INGRESO)
            .aggregate(ingresos=Sum("monto"))["ingresos"] or 0,
            2
        )        
        ahorro = ingresos - gastos        
        conteo = queryset.count()

        context.update({
            "selected_category": self.request.GET.get("categoria"),
            "modal_detail_id":"movimiento_detail",
            "modal_detail_container_id":"movimiento_detail_modal_container",
            "filtrando_por_fechas" : self.filtrando_por_fechas,
            "gastos": gastos,
            "ingresos": ingresos,
            "ahorro": ahorro,

            "conteo": conteo 
        })
        return context
    
class MovimientosEditDeleteView(RequireSuperUser, HtmxEditUpdateDeleteView):
    template_name = "cotton/ui/form.html"
    form_class = MovimientoForm
    success_url = reverse_lazy("movimiento_listar_registrar")
    queryset = Movimiento.objects.all()

    def save(self, form):
        movimiento = form.save()
        movimiento.registrado_por = self.request.user
        movimiento.save()
        return movimiento
    
    def get_retry_url(self):
        return reverse_lazy("movimiento_editar_eliminar", args=[self.kwargs['pk']])

  