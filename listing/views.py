from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingPostForm
from .models import ListingEdit
from .forms import ListingPostFormEdit
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic
from django.db import IntegrityError

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
            return redirect(reverse("listing:mylistings"))
        else:
            print("Not saved.")
            return render(request, 'listing/editlisting.html', context)
    else:
        context['title'] = listing.title
        context['description'] = listing.descrip
        context['stock'] = listing.stock
        context['my_listings'] = Listing.objects.filter(pk=pk)
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
            try:
                listing.title = formedit.cleaned_data['title']
                listing.descrip = formedit.cleaned_data['descrip']
                listing.stock=listing.stock + formedit.cleaned_data['stock']
                if formedit.cleaned_data['stock'] < 0:
                    formedit.add_error('stock', 'Restock amount must not be negative')
                    raise IntegrityError
                listing.price = formedit.cleaned_data['price']
                listing.save()
                form = ListingPostForm(instance=listing)
                inst = form.save(commit=False)
                inst.save()
                print('Form saved')
                context['form'] = form
                return redirect('/listing/mylistings')
            except IntegrityError:
                formedit.add_error(None, 'Could not edit form')
        else:
            print('Form not valid')
            formedit.add_error(None, 'Could not edit form')
        context['form'] = formedit
    return render(request, 'listing/editlisting.html', context)

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.delete()
    return redirect('listing:mylistings')

