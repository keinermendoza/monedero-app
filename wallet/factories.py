from random import choice
import factory
from wallet.models import  (
    Movimiento,
    CategoriaMovimiento
)

class CategoriaMovimientoFactory(factory.django.DjangoModelFactory):
    nombre = factory.Faker("word")
    tipo_movimiento = factory.LazyAttribute(lambda _: choice(["G", "I"]))

    class Meta:
        model = CategoriaMovimiento

class MovimientoFactory(factory.django.DjangoModelFactory):
    monto = factory.Faker("pydecimal", right_digits=2, max_value=999, min_value=1)
    descripcion = factory.Faker("sentence", nb_words=10, variable_nb_words=True)
    
    class Meta:
        model = Movimiento

    @factory.lazy_attribute
    def categoria(self):
        try:
            return CategoriaMovimiento.objects.order_by("?").first()  
        except CategoriaMovimiento.DoesNotExist:
            return CategoriaMovimiento.objects.create()