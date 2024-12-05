import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import GameServer

Rectangle {
    id: root

    GameServer {  //qmllint disable
        id: server
        onMessage: (msg) => {
            console.log(msg);
            messageReceiveText.text = msg;
        }
    }
    function closeServer() {
        server.close();
    }

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
                onClicked: server.connect(ipField.text, tokenField.text)
            }
        }

        Button {
            width: parent.width; height: parent.height * 0.5
            text: "send"
            onClicked: server.sendText(messageSendText.text)
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