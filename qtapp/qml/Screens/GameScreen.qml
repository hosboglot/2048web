import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import "../Views"
import ApiCaller
import GameManager


Page {
    id: root
    
    ColumnLayout {
      	anchors.fill: parent

     	Rectangle {
          	Layout.fillWidth: true
          	Layout.minimumHeight: 150
          	color: "black"
        }

      	Rectangle {
          	Layout.fillWidth: true
          	Layout.fillHeight: true
          	
            GameField {
                anchors.centerIn: parent
                width: parent.height
                height: parent.height
            }
        }
    }

    Component.onCompleted: GameManager.connect();

    focus: true
    Keys.onPressed: (event) => {
        if ([Qt.Key_W, Qt.Key_Up].includes(event.key)) {
            GameManager.processInput(GameManager.Up);
            return;
        }
        if ([Qt.Key_S, Qt.Key_Down].includes(event.key)) {
            GameManager.processInput(GameManager.Down);
            return;
        }
        if ([Qt.Key_A, Qt.Key_Left].includes(event.key)) {
            GameManager.processInput(GameManager.Left);
            return;
        }
        if ([Qt.Key_D, Qt.Key_Right].includes(event.key)) {
            GameManager.processInput(GameManager.Right);
            return;
        }
    }
}