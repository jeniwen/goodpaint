from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingPostForm
from django.http import Http404
from django.shortcuts import get_object_or_404

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
        context['form'] = form
    # for item in Listing.objects.all():
    #     item.delete()
    return render(request, 'listing/newlisting.html', context)


@login_required
def mylistings(request):
    context = {'my_listings': Listing.objects.filter(owner=request.user)}
    return render(request, 'listing/mylistings.html', context)

@login_required
def listing_edit(request,pk):
    context = {}
    listing = get_object_or_404(Listing, pk=pk)
    context['title'] = listing.title

    if request.method == "POST":
        form = ListingPostForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.save()
            context['form'] = form
    return render(request, 'listing/newlisting.html', context)



