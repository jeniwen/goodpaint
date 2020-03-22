from django.forms import ModelForm
from .models import Listing

class ListingPostForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['descrip', 'image', 'stock', 'dimensions', 'title', 'medium']
        
        
