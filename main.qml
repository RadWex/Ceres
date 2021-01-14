import QtQuick 2.0
import QtQuick.Scene3D 2.0
import QtQuick.Layouts 1.2
import QtMultimedia 5.0
import QtQuick.Controls 2.12

Item {
    id: mainview
    width: 600
    height: 500
    visible: true
    //anchors.fill: parent

    Image {
        id: coverImage
        //anchors.fill: parent
        //source: "images/albumcover.png"
    }

    //![1]
    Scene3D {
        id: scene3d
        multisample: true
        anchors.fill: parent
        //cameraAspectRatioMode: Scene3D.AutomaticAspectRatio
        aspects: ["render", "input", "logic"]
        Scene {
            set_parent: scene3d
            id: scene
        }
    }

/*

    Button {
        id: button
        anchors.top: parent.top
        text: "Render Capture"

        property var reply
        //property bool continuous : checkbox.checked
        //property int cid: 1

        function doRenderCapture()
        {
            reply = scene.requestRenderCapture()
            //console.log(reply)
            reply.completed.connect(onRenderCaptureComplete)
        }

        function onRenderCaptureComplete()
        {
            _renderCaptureProvider.model(reply.image)
            //image.source = "image://rendercapture/" + cid
            //reply.saveImage("capture" + cid + ".png")
            //cid++
            //if (continuous === true)
            //    doRenderCapture()
        }

        onClicked: doRenderCapture()
    }*/

/*
    Rectangle {
        id: object2d
        width: 500
        height: 700
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 10

        CorkBoards { }

        layer.enabled: true
    }
*/
}
