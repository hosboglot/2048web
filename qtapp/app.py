# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

import qml_interface.server  # noqa


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle('Universal')
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / 'qml' / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
