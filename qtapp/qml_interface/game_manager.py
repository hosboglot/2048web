from PySide6.QtCore import (
    QObject, Property,
    Slot, Signal, QEnum
)
from PySide6.QtQml import QmlElement, QmlSingleton

from game.server import WebsocketServer
from game.game import Game
from qml_interface.api_caller import ApiCaller
from qml_interface.tile_model import TileModel
from shared.game import Tile, UserInput, Snapshot, Direction

QML_IMPORT_NAME = "GameManager"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class GameManager(QObject):
    QEnum(Direction)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._server: WebsocketServer | None = None
        self._tile_model: TileModel | None = None

    @Slot()
    def connect(self):
        if self._server and self._server.is_alive():
            self._server.join()

        self._server = WebsocketServer()
        self._server.onConnected(self.connected.emit)
        self._server.onClosed(self.closed.emit)
        self._server.onMessage(self._onMessage)
        self._server.ip = ApiCaller().ip
        self._server.headers = {
            'Cookie': f'users_access_token={ApiCaller().accessToken}'
        }

        self._player_id = ApiCaller().getId()
        self._game = Game(self._player_id)
        self._game.onPackageToSend(self.sendInput)
        self._game.onSceneUpdated(self.updateScene)

        self._server.start()

    connected = Signal(bool)

    @Slot()
    def close(self):
        if self._server and self._server.is_alive():
            self._server.join()

        if self._game and self._game.is_alive():
            self._game._stop_flag = True
            self._game.join()

    closed = Signal(bool)

    @Slot(str)
    def sendText(self, message: str):
        self._server.send({
            'type': 'message',
            'content': message
            })

    def sendInput(self, cmd: UserInput):
        self._server.send({
            'type': 'command',
            'content': cmd.to_json()
            })

    @Property(TileModel)
    def tileModel(self):
        return self._tile_model

    @tileModel.setter
    def tileModel(self, val: TileModel):
        if self._tile_model != val:
            self._tile_model = val

    def updateScene(self, tiles: list[Tile]):
        self._tile_model.updateTiles(tiles)

    @Slot(int)
    def processInput(self, direction: int):
        self._game.user_input = Direction(direction)

    message = Signal(str)

    def _onMessage(self, data: dict):
        if data['type'] == 'snapshot':
            self._game.server_snapshot = Snapshot.from_json(data['content'])
            if not self._game.is_alive():
                self._game.start()
        elif data['type'] == 'message':
            self.message.emit(data['content'])
