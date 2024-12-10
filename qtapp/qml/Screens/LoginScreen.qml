import QtQuick
import QtQuick.Window
import QtQuick.Controls

import ApiCaller


Page {
    id: root
    title: "Авторизация"
    signal finished()

    Frame {
        id: frame
        anchors.centerIn: parent
        width: height;

        Column {
            id: col
            anchors.fill: parent
            spacing: 5

            LabelTextField {
                id: ipField
                width: parent.width
                labelText: "IP сервера"
                Component.onCompleted: text = ApiCaller.ip
            }

            LabelTextField {
                id: loginField
                width: parent.width
                labelText: "Логин"
            }

            LabelTextField {
                id: passwordField
                width: parent.width
                labelText: "Пароль"
                echoMode: TextField.Password
            }

            Button {
                id: confirmButton
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Вход"
                onClicked: {
                    ApiCaller.login(loginField.text, passwordField.text);
                }
            }
        }
    }

    Label {
        id: infoLabel
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: frame.bottom
        visible: text == ""
    }

    Connections {
        target: ApiCaller
        function onLogged(success) {
            if (success) {
                root.finished();
                return;
            } else {
                infoLabel.text = "Ошибка при подключении";
            }
        }
    }

    component LabelTextField: Rectangle {
        implicitWidth: Math.max(label.implicitWidth, textField.implicitWidth)
        implicitHeight: label.implicitHeight + textField.implicitHeight

        property alias labelText: label.text
        property alias text: textField.text
        property alias echoMode: textField.echoMode
        Label {
            id: label
            width: parent.width
        }
        TextField {
            id: textField
            width: parent.width
            anchors.top: label.bottom
        }
    }
}