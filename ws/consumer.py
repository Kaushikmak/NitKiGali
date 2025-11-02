# In ws/consumer.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from logservice import LogService
import sys
import uuid

# --- The "Waiting Pool" ---
waiting_pool = []


class MatchmakingConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.log = LogService(prefix="Matchmaker")
        self.log.write(f"New user connected to pool: {self.channel_name}", "INFO")
        await self.accept()
        
        if not waiting_pool:
            self.log.write("Waiting pool is empty. Adding user and waiting.", "DEBUG")
            waiting_pool.append(self.channel_name)
            await self.send_json({"status": "waiting"})
        else:

            self.log.write("User found in waiting pool. Creating pair.", "DEBUG")
            other_channel_name = waiting_pool.pop(0)

            room_name = uuid.uuid4().hex
            self.log.write(f"Pairing {self.channel_name} and {other_channel_name} in room: {room_name}", "INFO")


            redirect_message = {
                "type": "matchmaking.redirect",
                "room_name": room_name
            }

            await self.channel_layer.send(
                other_channel_name,
                redirect_message
            )

            await self.send_json({
                "type": "redirect",
                "room_name": room_name
            })
            

    async def disconnect(self, close_code):
        self.log.write(f"User disconnected from pool: {self.channel_name}", "INFO")

        if self.channel_name in waiting_pool:
            self.log.write("User was in pool, removing.", "DEBUG")
            waiting_pool.remove(self.channel_name)
        
        self.log.close()

    async def matchmaking_redirect(self, event):
        """
        This method is called by the channel_layer.send() command.
        It sends the redirect message down to the waiting client.
        """
        self.log.write(f"Sending redirect to waiting user: {self.channel_name}", "DEBUG")
        await self.send_json({
            "type": "redirect",
            "room_name": event['room_name']
        })

    # Helper
    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.log = LogService(prefix="ChatConsumer")

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        self.log.write(f"New connection for room: {self.room_name}", "INFO")

        try:

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            self.log.write(f"Connection accepted for room: {self.room_name}", "INFO")
            

            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": "[Partner has joined the chat]"}
            )

        except Exception as e:
            self.log.write(f"Failed to connect: {e}", "ERROR")
            await self.close()

    async def disconnect(self, close_code):
        self.log.write(f"Disconnected from room {self.room_name}", "INFO")
        try:
        
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": "[Partner has left the chat]"}
            )
            
         
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            self.log.write(f"Error on disconnect/discard: {e}", "ERROR")
        
        self.log.close()

    async def receive(self, text_data=None, bytes_data=None):
        self.log.write(f"Received message in room {self.room_name}", "DEBUG")
        try:
            data = json.loads(text_data)
            message = data.get('message', '')

      
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message', 
                    'message': message,
                }
            )
        except Exception as e:
            self.log.write(f"Error in receive(): {e}", "ERROR")

    async def chat_message(self, event):
        """
        Receives a message from the group and sends it to the client.
        """
        message = event['message']
        self.log.write(f"Sending group message to client: {message}", "DEBUG")
        await self.send_json({'message': message})

    # Helper
    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))