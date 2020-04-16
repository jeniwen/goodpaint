from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Room
from .models import Message
import pytz
from pytz import timezone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        user = self.scope['user']
        if user.is_authenticated:
          async_to_sync(self.channel_layer.group_add)(
              user.username,
              self.channel_name
          )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # timestamp = text_data_json['timestamp']
        room_owner = get_object_or_404(User, username=text_data_json['username'])
        room = get_object_or_404(Room, owner=room_owner)

        user = self.scope['user']

        handle = ''

        
        if user.is_authenticated:
            handle = user.username
        else:
            handle = 'Anonymous'

        # message = handle + message
         #save message to messages
        m = Message(room=room, handle=handle, message=message)
        print(str(m.timestamp.strftime("%Y-%m-%d %H:%M:%S")))
        eastern = timezone('US/Eastern')
        m.timestamp = m.timestamp.astimezone(eastern)
        m.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'timestamp':str(m.timestamp.astimezone(eastern).strftime("%B %d %Y %H:%M:%S")),
                'handle':handle
            }
        )

       
        

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        timestamp = event['timestamp']
        handle = event['handle']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'timestamp':timestamp,
            'handle':handle
        }))
    
    # Receive message from username group
    def logout_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'timestamp': event['timestamp'],
            'handle': event['handle'],



        }))
        self.close()
