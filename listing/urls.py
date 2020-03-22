from django.urls import path, include

from . import views

urlpatterns = [
    path('newlisting', views.newlisting, name='newlisting'),
    path('mylistings', views.mylistings, name='mylistings'),
    path('<int:pk>/edit/', views.listing_edit, name='listing_edit')

]
