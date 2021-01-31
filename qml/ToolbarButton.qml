import QtQuick 2.0
import QtQuick.Layouts 1.2
import QtMultimedia 5.0
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    property string source
    property string color
    palette {
        button: "transparent"
    }
    Image {
        id: image
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: parent
        sourceSize.height: parent.background.height - 6
        height: sourceSize.height
        source: parent.source
    }
    ColorOverlay {
        anchors.fill: image
        source: image
        color: parent.color
    }
}