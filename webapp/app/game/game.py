from fastapi import WebSocket
from fastapi.websockets import WebSocketState
import asyncio
from loguru import logger
from time import time_ns
from math import log2

from shared.game import UserInput, Grid, Snapshot


def time():
    '''time in ms'''
    return time_ns() // 1e6


class GameServer:
    def __init__(self, game_id: int):
        self._game_id = game_id
        self._connections: dict[int, WebSocket] = {}
        self._game_task: asyncio.Task | None = None
        self._players_count = 2
        self._player_inputs: dict[int, UserInput] = {}
        self._max_tiles: dict[int, int] = {}
        self._grid = Grid()

    async def connect_player(self, user_id: int, ws: WebSocket):
        await ws.accept()
        self._connections[user_id] = ws
        for player_ws in self._connections.values():
            await player_ws.send_json({'type': 'message',
                                       'content': f"Player {user_id} connected"})
        logger.info(f"Client {user_id} connected to game {self._game_id}")
        if len(self._connections) == self._players_count:
            self._game_task = asyncio.create_task(self._game_loop())

    async def disconnect_player(self, user_id: int):
        ws = self._connections[user_id]
        if ws.state == WebSocketState.CONNECTED:
            await ws.close()
        del self._connections[user_id]

    async def play(self, user_id: int):
        ws = self._connections[user_id]
        while True:
            message = await ws.receive_json()
            await self._process_player_input(ws, user_id, message)

    async def _process_player_input(self, ws: WebSocket, user_id: int, message):
        # logger.info(f'Message {message} from user {user_id} in game {self._game_id}')
        if message['type'] == 'command':
            self._player_inputs[user_id] = UserInput.from_json(message['content'])

    async def _send_snapshot(self, ws: WebSocket, user_id: int, snapshot: Snapshot):
        await ws.send_json({'type': 'snapshot', 'content': snapshot.to_json()})

    async def _game_loop(self):
        self._grid.spawn_start_tiles(self._connections.keys())
        self._max_tiles = dict(zip(self._connections.keys(), [2] * self._players_count))
        last_move_times = dict(zip(self._connections.keys(), [0] * self._players_count))
        last_simulated = time()
        last_tile_time = 0
        while self._connections:
            start_time = time()
            # каждые 30 мсек обновляем поле
            if time() - last_simulated > 30:
                last_simulated = time()

                # применяем все команды, которые пришли от игроков
                cmds = self._player_inputs.items()
                for id, cmd in cmds:
                    if cmd is not None:
                        if time() - last_move_times[id] > 500:
                            self._grid.move(id, cmd.direction)
                            last_move_times[id] = time()
                        self._player_inputs[id] = None

                # если игрок после хода обновил рекорд ...
                for id, val in self._grid.find_players_max_tile().items():
                    if self._max_tiles[id] < val:
                        self._max_tiles[id] = val
                        # накидываем ему log_2(max_val) - 1 новых плиток
                        for _ in range(int(log2(val)) - 1):
                            self._grid.insert_random_tile(id)

                # отправляем всем игрокам новое состояние игры
                snapshot = Snapshot(time(), self._grid.tiles())
                for id, ws in self._connections.items():
                    await self._send_snapshot(
                        ws, id, snapshot
                    )

            # каждую секунду спавним новую ничейную плитку
            if time() - last_tile_time > 1000:
                last_tile_time = time()
                self._grid.insert_random_tile(-1)

            # досыпаем оставшуюся часть тика
            frame_time = time() - start_time
            sleep_time = (30 - frame_time) / 1e3
            if sleep_time > 0:
                # print(sleep_time)
                await asyncio.sleep(sleep_time)

        self._player_inputs = {}
