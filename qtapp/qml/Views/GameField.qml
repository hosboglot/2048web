pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts

import "../Components"
import GameManager
import TileModel


Rectangle {
    id: root

    property int rows: 8
    property int columns: 8
    property real tileSize: (width - 10 - 5 * (rows - 1)) / rows

    Grid {
        id: backgroundTiles
        anchors.fill: parent
        anchors.margins: 5
        spacing: 5
        rows: root.rows
        columns: root.columns

        Repeater {
            model: parent.rows * parent.columns
            delegate: Tile {
                tileSize: root.tileSize
                color: "light grey"
            }
        }
    }

    Repeater {
        id: fieldTiles
        model: TileModel { // qmllint disable

        }
        delegate: TileDelegate {
            tileSize: root.tileSize
        }
    }

    Binding {
        target: GameManager
        property: "tileModel"
        value: fieldTiles.model
    }
}