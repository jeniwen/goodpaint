from django.shortcuts import render
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from .forms import AddToCartForm
from shopping_cart import views

from django.contrib.auth.decorators import login_required
from listing.models import Listing
# Create your views here.
@login_required
def info(request):
    context = {}
    context['username'] = request.user.username
    return render(request, 'browse/base.html', context)


def seelistings(request):
    context = {'all_listings': Listing.objects.all()}
    return render(request, 'browse/base.html', context)

def listing_detail(request, pk):
    listing =  get_object_or_404(Listing, pk=pk)
    context = {'listing': listing }
    if (request.method == 'POST'):
        print('post')
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # add_to_cart(request, pk, form.cleaned_data['quantity'])
            request.session['quantity'] = form.cleaned_data['quantity']
            request.session['pk'] = pk
            print('hi')
            return redirect('/shopping_cart/'+str(pk)+'/addtocart')
        else: print('form invalid')
    if (listing.stock <= 0):
        context['out_of_stock'] = True
            
    return render(request, 'browse/listing_detail.html', context)
