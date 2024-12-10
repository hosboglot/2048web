import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts


Rectangle {
    id: root

    required property var gameManager

    Column {
        anchors.fill: parent
        
        Row {
            width: parent.width; height: parent.height * 0.2
            Column {
                width: parent.width / 2; height: parent.height
                TextField {
                    id: ipField
                    width: parent.width; height: parent.height / 2
                    placeholderText: "IP"
                    text: "127.0.0.1:8000/game/1"
                }
                TextField {
                    id: tokenField
                    width: parent.width; height: parent.height / 2
                    placeholderText: "Access token"
                    text: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzM1NDAwMzYwfQ.cu9udc3RgA9Hj0NMy5S1brujxzDAriOy4yNoQXotw4Y"
                }
            }
            Button {
                width: parent.width / 2; height: parent.height
                text: "connect"
                onClicked: root.gameManager.connect(ipField.text, tokenField.text)
            }
        }

        Button {
            width: parent.width; height: parent.height * 0.5
            text: "send"
            onClicked: root.gameManager.sendText(messageSendText.text)
        }
        Row {
            width: parent.width; height: parent.height * 0.3
            TextArea {
                id: messageSendText
                width: parent.width / 2; height: parent.height
                text: "Hello"
            }
            TextArea {
                id: messageReceiveText
                width: parent.width / 2; height: parent.height
            }
        }
        
    }
}