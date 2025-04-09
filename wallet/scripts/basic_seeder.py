from random import randint
from django.contrib.auth import get_user_model
from wallet.factories import (
    MovimientoFactory,
    CategoriaMovimientoFactory
)
User = get_user_model()
# python manage.py runscript basic_seeder
def run():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="1234"
    )
    CategoriaMovimientoFactory.create_batch(10)
    MovimientoFactory.create_batch(200)