import QtQuick 2.0
import QtQuick.Scene3D 2.0
import QtQuick.Layouts 1.2
import QtMultimedia 5.0
import QtQuick.Controls 2.15

Item {
    id: mainview
    width: 550
    height: 500
    //visible: true
    //anchors.fill: parent
    property bool move : false
    property bool rotate : false

    Scene3D {
        id: scene3d
        multisample: true
        hoverEnabled: true
        anchors.fill: parent
        width: parent.width
        height: parent.height
        //cameraAspectRatioMode: Scene3D.AutomaticAspectRatio
        aspects: ["render", "input", "logic"]
        Scene {
            id: scene
            move: mainview.move
            rotate: mainview.rotate
        }
    }

    
    Rectangle {
        id: object2d
        color: "#33000000"

        width: 450
        height: 50
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 0

        Row {
            spacing: 10
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            ToolbarButton{
                id: buttonMove
                source: "../icons/move.png"
                onClicked: {
                    if(mainview.move)
                    {
                        mainview.move = false
                        buttonMove.color = "black"
                    }
                    else
                    {
                        if(mainview.rotate){
                            mainview.rotate = false
                            buttonRotate.color = "black"
                        }
                        mainview.move = true
                        buttonMove.color = "#007bd9"
                    }
                }
            }
            
            ToolbarButton{
                id: buttonRotate
                source: "../icons/rotation.png"
                onClicked: {
                    if(mainview.rotate)
                    {
                        mainview.rotate = false
                        buttonRotate.color = "black"
                    }
                    else
                    {
                        if(mainview.move){
                            mainview.move = false
                            buttonMove.color = "black"
                        }
                        mainview.rotate = true
                        buttonRotate.color = "#007bd9"
                    }
                }
            }

            ToolbarButton{
                id: buttonCenter
                source : "../icons/center.png"
                onClicked: {
                    scene.center_on_bed()
                }
            }

            ToolbarButton{
                id: buttonLayOnBed
                source : "../icons/lay.png"
                onClicked: {
                    scene.set_on_bed()
                }
            }
        }
        layer.enabled: true
    }

    /*
    Rectangle {
        visible: false
        id: loadingDarken
        width: parent.width
        height: parent.height
        color: "#33000000"

        Text {
            text:  qsTr("Loading...")
            font.pointSize: 30
            anchors.fill:parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    */
}
