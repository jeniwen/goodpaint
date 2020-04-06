from django.forms import ModelForm
from .models import Address

class AddressPostForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address1', 'address2', 'city','province','postal_code','country']