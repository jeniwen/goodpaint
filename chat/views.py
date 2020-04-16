from django.shortcuts import render
from .models import Room
from .models import Message
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from pytz import timezone

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
def chatroom(request, user):
    thisuser = get_object_or_404(User, username=user)
    room, created = Room.objects.get_or_create(owner=thisuser)
    messages = reversed(room.messages.order_by('-timestamp')[:50])
    messages_list = []
    eastern = timezone('US/Eastern')
    for m in messages:

        single_message = {
            'msg:': "" + m.message,
            'hndle': m.handle,
            'timestamp' : m.timestamp.astimezone(eastern).strftime("%B %d %Y %H:%M:%S")
        }
        single_message['msg'] = m.message
        single_message['is_me'] = m.handle == user
        messages_list.append(single_message)
    return render(request, 'chat/chatroom.html', {
        'room_name': user,
        'username':user,
        'msgs': messages_list
    })

@login_required
def mymessages(request):
    print("hi")
    return redirect('/chat/'+str(request.user))