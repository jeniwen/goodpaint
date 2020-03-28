from django.urls import path, include

from . import views

app_name ='shopping_cart'
urlpatterns = [
    path('', views.showcart, name='mycart'),
    path('<int:pk>/addtocart', views.addtocart, name='addtocart'),
    path('<int:pk>/deletefromcart', views.deletefromcart, name='deletefromcart')
]
