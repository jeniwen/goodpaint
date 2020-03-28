from django.forms import ModelForm
from .models import Listing
from .models import ListingEdit


class ListingPostForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['descrip', 'image', 'stock', 'dimensions1', 'dimensions2', 'unit', 'title', 'medium', 'price']
        
        
class ListingPostFormEdit(ModelForm):
    class Meta:
        model = ListingEdit
        fields = ['descrip', 'title', 'stock', 'price']