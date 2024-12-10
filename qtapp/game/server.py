from typing import Callable
from threading import Thread
from websockets.sync.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosed
import json


class WebsocketServer(Thread):
    def __init__(self):
        super().__init__()
        self._ws: ClientConnection | None = None
        self.ip: str = ''
        self.headers: dict[str, str] = {}

        self._close = False
        self._conn_cback: Callable[[bool], None] = None
        self._msg_cback: Callable[[dict], None] = None
        self._close_cback: Callable[[bool], None] = None

    def run(self):
        res = self._connect()
        if self._conn_cback:
            self._conn_cback(res)
        if not res:
            return

        close_res = self._listen()

        if self._ws:
            self._ws.close()
        if self._close_cback:
            self._close_cback(close_res)

    def join(self):
        if self._ws:
            self._ws.close()
        self._close = True
        super().join()

    def onConnected(self, func: Callable[[bool], None]):
        '''
        Callback to be called after connection attempt

        Calls with True, if connected successfully
        '''
        self._conn_cback = func

    def onMessage(self, func: Callable[[dict], None]):
        '''Callback to be called on message receive'''
        self._msg_cback = func

    def onClosed(self, func: Callable[[bool], None]):
        '''
        Callback to be called on connection closed

        Calls with True, if connection closed as expected
        '''
        self._close_cback = func

    def send(self, message_dict: dict):
        '''Send message'''
        msg = json.dumps(message_dict)
        if self._ws:
            self._ws.send(msg)

    def _connect(self) -> bool:
        try:
            self._ws = connect(
                f'ws://{self.ip}/game/1',
                additional_headers=self.headers,
                open_timeout=5)
        except BaseException as e:
            print(e)
            return False
        return True

    def _onMessage(self, message: str):
        msg_dict: dict = json.loads(message)
        if self._msg_cback:
            self._msg_cback(msg_dict)

    def _listen(self) -> bool:
        try:
            while not self._close:
                try:
                    msg = self._ws.recv(0.5)
                    if msg:
                        self._onMessage(msg)
                except TimeoutError:
                    pass
        except ConnectionClosed:
            return False
        return True
