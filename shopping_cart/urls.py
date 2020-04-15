from django.urls import path, include

from . import views

app_name ='shopping_cart'
urlpatterns = [
    path('', views.showcart, name='mycart'),
    path('<int:pk>/addtocart', views.addtocart, name='addtocart'),
    path('<int:pk>/deletefromcart', views.deletefromcart, name='deletefromcart'),
    path('pastorders', views.pastorders, name='pastorders'),
    path('pastorders/<int:ref_code>', views.pastorders_view, name='pastorders_view')
]
