from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from listing.models import Listing
from .models import OrderItem
from .models import Order
from .models import generate_order_id
from django.db import IntegrityError

#With help from https://www.youtube.com/watch?v=vccUP3jdpBg
# Create your views here.
@login_required
def showcart(request):
    context = {}
    user = get_object_or_404(User, username=request.user)
    user_order, status = Order.objects.get_or_create(owner=user, is_ordered=False)
    context['user_order'] = user_order.items.all()
    context['total'] = user_order.get_cart_total()
    context['order_num'] = user_order.ref_code
    context['user'] = request.user
    context['currentcart'] = False

    return render(request, 'shopping_cart/mycart.html', context)

@login_required
def pastorders_view(request, ref_code):
    context = {}
    user = get_object_or_404(User, username=request.user)
    user_order = get_object_or_404(Order, owner=user, ref_code=ref_code)
    context['user_order'] = user_order.items.all()
    context['total'] = user_order.get_cart_total()
    context['order_num'] = user_order.ref_code
    context['user'] = request.user
    
    return render(request, 'shopping_cart/mycart.html', context)

@login_required
def pastorders(request):
    context = {}
    user = get_object_or_404(User, username=request.user)
    user_orders = Order.objects.filter(owner=user, is_ordered=True).order_by('-date_ordered')

    orders_dict = {}
    # queryset = queryset.order_by('-id')
    for ord in user_orders:
        # print(ord)
        order_info = {}
        order_info['ref_code'] = ord.ref_code
        order_info['total'] = ord.get_grand_total()
        order_info['order_date'] = ord.date_ordered
        order_info['num_items'] = ord.get_cart_num_items()
        orders_dict[ord.ref_code] = order_info
    context['dict'] = orders_dict

    return render(request, 'shopping_cart/pastorders.html', context)


@login_required
def addtocart(request, pk):
    context = {}
    
    # print('hello ' + str(request.session['quantity']) + " " + str(pk))

    #Start building OrderItem
    user = get_object_or_404(User, username=request.user)
    listing = get_object_or_404(Listing, pk=pk)
    if (listing.stock <= 0):
        return redirect('/browse/', context)
    else:
        listing.stock = listing.stock - 1
        listing.save()
    # quantity = request.session['quantity']
    try:
        order_item = OrderItem(product=listing)
        order_item.save()
        user_order, status = Order.objects.get_or_create(owner=user, is_ordered=False)
        user_order.items.add(order_item)
        print(user_order.get_cart_total())
        if status or user_order.ref_code == '' or user_order.ref_code is None: #
            user_order.ref_code = generate_order_id()
            user_order.save()
        print('Items added.')
    except IntegrityError:
        print('Item already in cart!')
        context['ierror'] = 'Item already in cart!'
        return redirect('/browse/', context)
    context['user_order'] = user_order.items.all()
    context['total'] = user_order.get_cart_total()
    return redirect('/shopping_cart/', context)

    # return render(request, 'shopping_cart/mycart.html', context)

def deletefromcart(request, pk):
    context = {}
    user = get_object_or_404(User, username=request.user)
    user_order = get_object_or_404(Order, owner=user, is_ordered=False)
    order_item = get_object_or_404(OrderItem,pk=pk)
    order_item.product.stock = order_item.product.stock+1
    order_item.product.save()
    if order_item in user_order.get_cart_items():
        print('order Item exists.')
        user_order.items.remove(order_item)
        user_order.save()
    else: 
        print('Could not find order item')
        return redirect('/shopping_cart/')
    context = {}
    context['user_order'] = user_order.items.all()
    context['total'] = user_order.get_cart_total()
    return redirect('/shopping_cart/')



