import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Tile {
    id: root

    required property var model

    x: root.calculateX(model.x); y: root.calculateY(model.y)

    function calculateX(x) {
        if (x === 0) return 5;
        else return 5 + x * (5 + tileSize);
    }
    function calculateY(y) {
        return calculateX(y);
    }

    value: root.model.value
    color: model.color

    // Connections {
    //     target: root.model
    //     function onPrevious() {
    //         console.log("hi")
    //     }
    // }
}