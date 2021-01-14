import QtQuick 2.2
import Qt3D.Core 2.0
import Qt3D.Render 2.15
import Qt3D.Input 2.0
import Qt3D.Extras 2.15


Entity {
    id: rootNode
    property var set_parent
    property var reply
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

    function requestRenderCapture()
    {
        return quadViewportFrameGraph.renCap.requestCapture()
    }

    components: [quadViewportFrameGraph, inputSettings]

    QuadViewportFrameGraph {
        id: quadViewportFrameGraph
        topLeftCamera: cameraSet.cameras[0]
        bottomRightCamera: cameraSet.cameras[1]
    }

    // Event Source will be set by the Qt3DQuickWindow
    InputSettings { id: inputSettings }

    OrbitCameraController {
            lookSpeed: 1000
            linearSpeed: 1000
            camera: camera
        }


    Entity {
        id: cameraSet
        property var cameras: [virtual_camera, camera]

        Camera {
            id: camera
            projectionType: CameraLens.OrthographicProjection
            left: -set_parent.width/4
            right: set_parent.width/4
            bottom: -set_parent.height/4
            top: set_parent.height/4
            nearPlane: 0.1
            farPlane: 1000.0
            position: Qt.vector3d(100.0, -100.0, 300.0)
            //upVector: Qt.vector3d(-100.0, 0.0, -100.0)
            viewCenter: Qt.vector3d(100.0, 100.0, 0.0)
        }

        Camera {
            id: virtual_camera
            projectionType: CameraLens.OrthographicProjection

            nearPlane: 0.1
            farPlane: 1000.0
            left: -set_parent.width/4
            right: set_parent.width/4
            bottom: -set_parent.height/4
            top: set_parent.height/4
            position: Qt.vector3d(100.0, 100.0, 100.0)
            //upVector: Qt.vector3d(0.0, 1.0, 0.0)
            viewCenter: Qt.vector3d(100.0, 100.0, 0.0)
        }
    }

    function printHits(desc, hits) {
            console.log(desc, hits.length)
            for (var i=0; i<hits.length; i++) {
                console.log("  " + hits[i].entity.objectName, hits[i].distance,
                            hits[i].worldIntersection.x, hits[i].worldIntersection.y, hits[i].worldIntersection.z)
            }
        }

    RayCaster {
            id: raycaster
            origin: Qt.vector3d(0, 0, 4)
            direction: Qt.vector3d(0., 0., -1.)
            length: 5

            onHitsChanged: printHits("Model hits", hits)
        }

    Entity {
        id: sceneRoot

/*
        ScreenRayCaster {
                id: screenRayCaster

                onHitsChanged: printHits("Screen hits", hits)
            }
        MouseHandler {
                id: mouseHandler
                sourceDevice:  MouseDevice {}
                onReleased: { screenRayCaster.trigger(Qt.point(mouse.x, mouse.y))
                console.log("dzoala")}
            }*/

        //Component.onCompleted: {doRenderCapture()}//do poprawy
        PhongMaterial {
                    id: material
                    ambient: "gray"
                    diffuse: "gray"
                    specular: "white"
                }

        Mesh {
            id: circleMesh
            source: r_manager.modelChange
            onSourceChanged: doRenderCapture()
        }

        Transform{
            id: circleTransform
            translation.x: r_manager.x
            translation.y: r_manager.y
            translation.z: r_manager.z
            rotationX: r_manager.x_rot
            rotationY: r_manager.y_rot
            rotationZ: r_manager.z_rot
            scale3D: Qt.vector3d(r_manager.x_scale,r_manager.y_scale,r_manager.z_scale)
            //PropertyChanges {
                //target: qmlNote
              //  onNoteChanged: doRenderCapture
            //}
            onScale3DChanged: doRenderCapture()
            onRotationXChanged: doRenderCapture()
            onTranslationChanged: doRenderCapture()

        }

        Entity {
            id: circleEntity
            components: [circleMesh, material, circleTransform/*, screenRayCaster, mouseHandler*/]
        }


    } // sceneRoot
    Entity{
        components: [
        PointLight{
                color: "red"
                intensity: 10
                                constantAttenuation: 1.0
                                linearAttenuation: 0.0
                                quadraticAttenuation: 0.0025
        }, Transform {
                translation: Qt.vector3d(0.0, 50.0, 30.0)
            }
        ]
    }
    Entity{
        components: [
        PointLight{
                color: "green"
                intensity: 10
                                constantAttenuation: 1.0
                                linearAttenuation: 0.0
                                quadraticAttenuation: 0.0025
        }, Transform {
                translation: Qt.vector3d(0.0, -50.0, 50.0)
            }
        ]
    }
    Entity{
        components: [
        PointLight{
                color: "green"
                intensity: 10
                                constantAttenuation: 1.0
                                linearAttenuation: 0.0
                                quadraticAttenuation: 0.0025
        }, Transform {
                translation: Qt.vector3d(0.0, -50.0, -50.0)
            }
        ]
    }

        GridEntity {
                id: raydisplay
                sizeX: 300
                sizeY: 200
            }

} // rootNode
