import requests
import json

from PySide6.QtCore import (
    QObject, QPointF,
    Slot, Signal, Property
)
from PySide6.QtQml import QmlElement, QmlSingleton

from config import config

QML_IMPORT_NAME = "ApiCaller"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class ApiCaller(QObject):
    _ip = config.ip
    _is_logged = False
    _token = config.access_token

    def __init__(self, parent=None):
        super().__init__(parent)

    ipChanged = Signal(str)

    @Property(str, notify=ipChanged)
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, val):
        if self._ip != val:
            self._ip = val
            self.ipChanged.emit(val)

    accessTokenChanged = Signal(str)

    @Property(str, notify=accessTokenChanged)
    def accessToken(self):
        return self._token

    @accessToken.setter
    def accessToken(self, val):
        if self._token != val:
            self._token = val
            self.accessTokenChanged.emit(val)

    logged = Signal(bool)

    @Property(bool, notify=logged)
    def isLogged(self):
        return self._is_logged

    @Slot(str, str)
    def login(self, login: str, password: str):
        response = requests.post(
            f'http://{self.ip}/user/login/',
            json={
                "name": login,
                "password": password
            }
        )

        if not response.status_code == 200:
            self.logged.emit(False)
            return

        token = response.cookies['users_access_token']
        self.accessToken = token
        # print(token)
        self.logged.emit(True)

    @Slot()
    def getId(self):
        response = requests.get(
            f'http://{self.ip}/user/me/',
            cookies={'users_access_token': self.accessToken},
            timeout=3
        )

        return response.json()['id']
