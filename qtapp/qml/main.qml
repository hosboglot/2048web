import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import "Screens" as Screens


ApplicationWindow {
    id: root
    width: 640
    height: 640
    visible: true
    title: qsTr("2048")
    minimumWidth: 640
    minimumHeight: 640

    onClosing: testScreen.closeServer()
    Screens.TestEcho {
        id: testScreen
        anchors.fill: parent
    }

}
