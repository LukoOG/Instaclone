import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.dm_id = self.scope['url_route']['kwargs']['dm']
        self.room_group_name = f'dm_{self.dm_id}'
        print(self)
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                    self.channel_name)
        self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': f'dm {self.dm_id} connected'
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print('socket:', text_data_json)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'dm_message',
            'message': message
        })

    # self.send(text_data=json.dumps({"message": message}))
    def dm_message(self, event):
        message = event['message']
        print('received event:', event)
        self.send(text_data=json.dumps({'type': 'dm', 'message': message}))
