from PySide6.QtCore import (
    QObject, QPointF,
    Slot, Signal, Property
)
from PySide6.QtQml import QmlElement

from game.server import GameServer as BackServer

QML_IMPORT_NAME = "GameServer"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class GameServer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._back = BackServer()

    @Slot(str, str)
    def connect(self, ip: str, token: str):
        self._back.connect(
            ip,
            {'Cookie': f'users_access_token={token}'})
        self._back.addCallback(self._onMessage)

    @Slot()
    def close(self):
        self._back.close()

    message = Signal(str)

    def _onMessage(self, data: dict):
        self.message.emit(data['message'])

    @Slot(str)
    def sendText(self, message: str):
        self._back.send({'message': message})
