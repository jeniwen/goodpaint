from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingPostForm
from .models import ListingEdit
from .forms import ListingPostFormEdit
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

class MyListingsIndexView(generic.ListView):
    template_name = 'listing/mylistings'
    context_object_name = 'all_listings'

    def get_queryset(self):
        return Listing.objects.filter(owner=request.user)



@login_required
def newlisting(request):
    # context = {'photos': InstaPost.objects.all()}
    context = {'prev_listings': Listing.objects.all()}
    if request.method == 'POST':
        form = ListingPostForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.owner = request.user
            inst.save()
            return redirect('listing:mylistings')

        context['form'] = form
    # for item in Listing.objects.all():
    #     item.delete()
    return render(request, 'listing/newlisting.html', context)


@login_required
def mylistings(request):
    context = {'my_listings': Listing.objects.filter(owner=request.user)}
    return render(request, 'listing/mylistings.html', context)

@login_required
def listing_edit2(request,pk):
    context = {}
    listing = get_object_or_404(Listing, pk=pk)
    context['title'] = listing.title
    context['description'] = listing.descrip
    context['stock'] = listing.stock
    context['my_listings'] = Listing.objects.filter(pk=pk)
    

    if request.method == "POST":
        form = ListingPostForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.title = request.POST.get('title')
            edit.descrip = request.POST.get('descrip')
            edit.stock = request.POST.get('stock')
            edit.save()
            context['form'] = form
            print("Succesfully saved.")
        else:
            print("Not saved.")
        # context['my_listings'] = Listing.objects.filter(owner=request.user)
        return render(request, 'listing/editlisting.html', context)
    else:
        return render(request, 'listing/editlisting.html', context)

@login_required
def listing_edit(request,pk):
    context = {}
    listing = get_object_or_404(Listing, pk=pk)
    # context['title'] = listing.title
    context['listing'] = listing

    if request.method == "POST":
        formedit = ListingPostFormEdit(request.POST)
        if formedit.is_valid():
            listing.title = request.POST.get('title')
            # listing.image = request.FILES.get('image')
            listing.description = request.POST.get('descrip')
            listing.stock=request.POST.get('stock')
            listing.price = request.POST.get('price')
            form = ListingPostForm(instance=listing)
            inst = form.save(commit=False)
            inst.save()
            print('Form saved')
            context['form'] = form
            return redirect('/listing/mylistings')
        print('Form not valid')
    
    return render(request, 'listing/editlisting.html', context)

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.delete()
    return redirect('listing:mylistings')

