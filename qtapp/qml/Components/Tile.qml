import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    radius: width / 10

    required property real tileSize
    width: root.tileSize; height: width

    property alias value: valueLabel.text

    Label {
        id: valueLabel
        anchors.centerIn: parent
        color: "white"
    }
}