from django.urls import path, include

from . import views
app_name ='chat'
urlpatterns = [
    path('<str:user>', views.chatroom, name='chatroom'),
    path('my/messages', views.mymessages, name='mymessages')
    # path('<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    # path('<int:pk>/delete/', views.listing_delete, name='listing_delete')


]