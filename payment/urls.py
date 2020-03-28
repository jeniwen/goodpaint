from django.urls import path, include

from . import views
app_name ='payment'
urlpatterns = [
    path('pay', views.do_payment, name='pay')
    # path('mylistings', views.mylistings, name='mylistings'),
    # path('<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    # path('<int:pk>/delete/', views.listing_delete, name='listing_delete')
]
