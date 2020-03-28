from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from listing.models import Listing
from shopping_cart.models import OrderItem
from shopping_cart.models import Order
from django.db import IntegrityError

# Create your views here.
def do_payment(request):
    context = {}
    print(get_user_pending_order(request))
    print(get_user_pending_order(request).ref_code)
    return render(request, 'payment/checkout.html',context)

def get_user_pending_order(request):
    # get order for the correct user
    user = get_object_or_404(User, username=request.user)
    order = Order.objects.filter(owner=user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        print("Order exists.")
        return order[0]
    return 0
