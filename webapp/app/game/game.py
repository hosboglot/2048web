from fastapi import WebSocket
import asyncio
from loguru import logger


class GameServer:
    def __init__(self, game_id: int):
        self._game_id = game_id
        self._connections: dict[int, WebSocket] = {}
        self._game_event = asyncio.Event()
        self._end_event = asyncio.Event()

    async def connect_player(self, user_id: int, ws: WebSocket):
        await ws.accept()
        self._connections[user_id] = ws
        for player_ws in self._connections.values():
            await player_ws.send_json({'message': f"Player {user_id} connected"})
        logger.info(f"Client {user_id} connected to game {self._game_id}")
        # asyncio.create_task(self.wait_player_input(user_id))

    async def play(self, user_id: int):
        ws = self._connections[user_id]
        while not self._end_event.is_set():
            message = await ws.receive_json()
            await self.process_player_input(ws, user_id, message)

    async def process_player_input(self, ws: WebSocket, user_id: int, message):
        logger.info(f'Message {message} from user {user_id} in game {self._game_id}')
        await ws.send_json(message)

    async def wait_for_end(self):
        await self._end_event.wait()
