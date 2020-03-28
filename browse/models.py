from django.db import models
from shopping_cart.models import OrderItem
from django.forms import ModelForm

def validate_gt_zero(value):
    if value <= 0:
        raise ValidationError(
            ('Value must be greater than zero.'),
            params={'value': value},
        )
