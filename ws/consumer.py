from channels.generic.websocket import AsyncWebsocketConsumer
import json
from logservice import LogService
import sys
import uuid
import redis

# --- Connect to Redis for your Matchmaking Pool ---
try:
    redis_client = redis.Redis(host='redis', port=6379, db=2, decode_responses=True)
    redis_client.ping()
    print("[Redis] Connected to Redis for matchmaking pool.")
except Exception as e:
    print(f"[Redis] ERROR: Could not connect to Redis. {e}")
    redis_client = None

WAITING_POOL_KEY = "matchmaking_waiting_pool"

class MatchmakingConsumer(AsyncWebsocketConsumer):
    # ... (No changes to the rest of this class) ...
    async def connect(self):
        self.log = LogService(prefix="Matchmaker")
        self.log.write(f"New user connected to pool: {self.channel_name}", "INFO")
        
        if redis_client is None:
            self.log.write("FATAL: Redis client is not connected.", "ERROR")
            await self.close()
            return

        await self.accept()

        try:
            other_channel_name = redis_client.lpop(WAITING_POOL_KEY)
            
            if other_channel_name is None:
                self.log.write("Waiting pool is empty. Adding user and waiting.", "DEBUG")
                redis_client.rpush(WAITING_POOL_KEY, self.channel_name)
                await self.send_json({"status": "waiting"})
            
            else:
                self.log.write(f"User found in pool: {other_channel_name}. Creating pair.", "DEBUG")
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
        except Exception as e:
            self.log.write(f"Error during matchmaking: {e}", "ERROR")
            await self.close()

    async def disconnect(self, close_code):
        self.log.write(f"User disconnected from pool: {self.channel_name}", "INFO")
        if redis_client:
            try:
                redis_client.lrem(WAITING_POOL_KEY, 0, self.channel_name)
                self.log.write("User removed from waiting pool.", "DEBUG")
            except Exception as e:
                self.log.write(f"Error removing user from Redis pool: {e}", "ERROR")
        self.log.close()

    async def matchmaking_redirect(self, event):
        self.log.write(f"Sending redirect to waiting user: {self.channel_name}", "DEBUG")
        await self.send_json({
            "type": "redirect",
            "room_name": event['room_name']
        })

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))

class ChatConsumer(AsyncWebsocketConsumer):
    # ... (No changes to this class) ...
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
                {'type': 'chat_message', 'message': message}
            )
        except Exception as e:
            self.log.write(f"Error in receive(): {e}", "ERROR")

    async def chat_message(self, event):
        message = event['message']
        self.log.write(f"Sending group message to client: {message}", "DEBUG")
        await self.send_json({'message': message})

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))