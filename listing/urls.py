from django.urls import path, include

from . import views
app_name ='listing'

urlpatterns = [
    path('newlisting', views.newlisting, name='newlisting'),
    path('mylistings', views.mylistings, name='mylistings'),
    path('<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    path('<int:pk>/delete/', views.listing_delete, name='listing_delete')


]
