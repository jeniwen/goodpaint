from django.urls import path, include

from . import views
app_name ='payment'
urlpatterns = [
    path('<int:pk>/pay', views.do_payment, name='pay'),
    path('getaddress',views.get_address, name='getaddress'),
    path('<int:pk>/<token>/order_complete', views.order_complete, name='order_complete')
    # path('mylistings', views.mylistings, name='mylistings'),

]
