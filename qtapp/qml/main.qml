import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import "Screens" as Screens
import GameManager
import ApiCaller


ApplicationWindow {
    id: root
    visible: true
    title: qsTr("2048")
    minimumWidth: 640
    minimumHeight: 640

    onClosing: GameManager.close()

    StackView {
        id: stackView
        anchors.fill: parent
        focus: true
        initialItem: ApiCaller.accessToken == "" ? loginScreen : gameScreen
    }

    Component {
        id: loginScreen
        Screens.LoginScreen {
            onFinished: StackView.view.push("Screens/GameScreen.qml")
        }
    }
    Component {
        id: gameScreen
        Screens.GameScreen {
            
        }
    }
}
