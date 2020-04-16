from django.shortcuts import render
from .models import Room
from .models import Message
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
def chatroom(request, user):
    thisuser = get_object_or_404(User, username=request.user)
    room, created = Room.objects.get_or_create(owner=thisuser)
    messages = reversed(room.messages.order_by('-timestamp')[:50])
    return render(request, 'chat/chatroom.html', {
        'room_name': user,
        'username':user
    })

@login_required
def mymessages(request):
    print("hi")
    return redirect('/chat/'+str(request.user))