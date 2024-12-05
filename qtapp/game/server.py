from typing import Callable
from threading import Thread
from websockets.sync.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosed
import json


class GameServer:
    def __init__(self):
        self._thread: Thread | None = None
        self._ws: ClientConnection | None = None
        self._callbacks: list[Callable[[dict], None]] = []

    def connect(self, ip: str, headers: dict[str, str]):
        self._thread = Thread(target=self._listen)
        self._ws = connect(
            f'ws://{ip}',
            additional_headers=headers)
        self._thread.start()

    def close(self):
        self._ws.close()
        self._ws = None
        self._thread.join()
        self._thread = None

    def addCallback(self, func: Callable[[dict], None]):
        self._callbacks.append(func)

    def removeCallback(self, func: Callable[[dict], None]):
        self._callbacks.remove(func)

    def send(self, message_dict: dict):
        msg = json.dumps(message_dict)
        self._ws.send(msg)

    def _onMessage(self, message: str):
        msg_dict: dict = json.loads(message)
        for cb in self._callbacks:
            cb(msg_dict)

    def _listen(self):
        try:
            while True:
                msg = self._ws.recv()
                self._onMessage(msg)
        except ConnectionClosed:
            pass
        finally:
            if self._ws:
                self._ws.close()
                self._ws = None
