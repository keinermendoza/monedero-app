from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    CategoriaMovimientoView,
    CategoriaMovimientoEditDeleteView,
    MovimientosView,
    MovimientosEditDeleteView
)

urlpatterns = [
    path('', RedirectView.as_view(url="movimientos", permanent=True)),
    path('categorias', CategoriaMovimientoView.as_view(), name="categoria_listar_registrar"),
    path('categorias/<int:pk>', CategoriaMovimientoEditDeleteView.as_view(), name="categoria_editar_eliminar"),
    path('movimientos', MovimientosView.as_view(), name="movimiento_listar_registrar"),
    path('movimientos/<int:pk>', MovimientosEditDeleteView.as_view(), name="movimiento_editar_eliminar"),
]