from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from listing.models import Listing
from .forms import AddressPostForm
from shopping_cart.models import OrderItem
from shopping_cart.models import Order
from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages
import stripe
import datetime
from django.urls import reverse

from .models import Transaction
from .models import Address




stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
@login_required
def get_address(request):
    context = {}
    if request.method == 'POST':
        form = AddressPostForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.save()
            print(addr.name, addr.country)
            # request.session['address'] = addr
        return redirect(reverse('payment:pay', kwargs={'pk': addr.id}))
    else:
        form=AddressPostForm()
        context['form']=form
        order = get_user_pending_order(request)
        context['order'] = order
        return render(request, 'payment/addressform.html',context)

@login_required
def do_payment(request, pk):
    #help from: https://testdriven.io/blog/django-stripe-tutorial/
    context = {}
    # print(get_user_pending_order(request).ref_code)
    order = get_user_pending_order(request)
    context['order'] = order
    context['key'] = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        token = request.POST.get('stripeToken',False)
        print(token)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=round(100*order.get_grand_total()),
                    currency='cad',
                    description=order.ref_code,
                    source = token,
                )
               
                return redirect(reverse('payment:order_complete',kwargs={'token': token, 'pk':pk}))
            except stripe.error.CardError as e:
                messages.info(request, "Your card has been declined.")
    return render(request, 'payment/checkout.html',context)

@login_required
def get_user_pending_order(request):
    # get order for the correct user
    user = get_object_or_404(User, username=request.user)
    order = Order.objects.filter(owner=user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        print("Order exists.")
        return order[0]
    return None

def order_complete(request, token,pk):
    context = {}
    user = get_object_or_404(User, username=request.user)
    order = get_object_or_404(Order, owner=user, is_ordered=False)
    address = get_object_or_404(Address, id=pk)

    # transaction = Transaction(user, )
    print(user)
    print(order)
    print("order complete " + token)
    print(address)

    order.is_ordered=True
    order.date_ordered=datetime.datetime.now()
    order.save()
    order_items = order.items.all()
    order_items.update(is_ordered = True, date_ordered = datetime.datetime.now())
    # print(request.session['address'])
    transaction = Transaction(
        user = user,
        token = token,
        order_id=order.ref_code,
        amount=order.get_grand_total(),
        success=True,
        shipping_address = address,
        timestamp =  datetime.datetime.now()
    )
    return render(request, 'payment/ordercomplete.html', context)