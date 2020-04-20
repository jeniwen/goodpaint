from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.seelistings, name='browse'),
    path('<int:pk>/details/', views.listing_detail, name='listing_detail')
]
