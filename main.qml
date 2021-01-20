import QtQuick 2.0
import QtQuick.Scene3D 2.0
import QtQuick.Layouts 1.2
import QtMultimedia 5.0
import QtQuick.Controls 2.15

Item {
    id: mainview
    width: 500
    height: 500
    visible: true
    //anchors.fill: parent
    property bool move : false
    //![1]
    Scene3D {
        id: scene3d
        multisample: true
        //anchors.fill: parent
        width: parent.width
        height: parent.height
        //cameraAspectRatioMode: Scene3D.AutomaticAspectRatio
        aspects: ["render", "input", "logic"]
        Scene {
            set_parent: scene3d
            id: scene
            move: mainview.move
        }
    }


    Rectangle {
        id: object2d
        color: "#33000000"

        width: 500
        height: 50
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 0
        Button{
            icon.source: "icons/move.png"
            anchors.top: parent.top
            display: AbstractButton.IconOnly
            anchors.bottom: parent.bottom
            onClicked: {
                if(mainview.move)
                    mainview.move = false
                else
                    mainview.move = true
            }
        }

        layer.enabled: true
    }

}
