import QtQuick 2.2
import Qt3D.Core 2.0
import Qt3D.Render 2.15
import Qt3D.Input 2.0
import Qt3D.Extras 2.15


Entity {
    id: rootNode
    property bool move: true
    property var set_parent
    property var reply
    function doRenderCapture()
    {
        reply = scene.requestRenderCapture()
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
            linearSpeed: 1500
            camera: camera
        }

    Entity {
        id: cameraSet
        property var cameras: [virtual_camera, camera]

        Camera {
            id: camera
            projectionType: CameraLens.PerspectiveProjection
            fieldOfView: 30
            aspectRatio: 16 / 9
            nearPlane: 0.1
            farPlane: 1000.0
            position: Qt.vector3d(100.0, 300.0, 300.0)
            //upVector: Qt.vector3d(-100.0, 0.0, -100.0)
            viewCenter: Qt.vector3d(100.0, 0.0, -100.0)
        }

        Camera {
            id: virtual_camera
            projectionType: CameraLens.OrthographicProjection

            nearPlane: 0.1
            farPlane: 1000.0
            left: -200/1.9
            right: 200/1.9
            bottom: -200/1.9
            top: 200/1.9
            position: Qt.vector3d(100.0, 100.0, -100.0)
            //upVector: Qt.vector3d(0.0, 1.0, 0.0)
            viewCenter: Qt.vector3d(100.0, 0.0, -100.0)
        }
    }
    /*
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

        ScreenRayCaster {
                id: screenRayCaster

                onHitsChanged: printHits("Screen hits", hits)
            }
        MouseHandler {
                id: mouseHandler
                sourceDevice:  MouseDevice {}
                onReleased: { screenRayCaster.trigger(Qt.point(mouse.x, mouse.y))
                console.log("dzoala")}
    */


    //Buffer{
   //     data:  geometryLoaded(modelMesh)
    //}

    Entity {
        id: sceneRoot

        //Component.onCompleted: {doRenderCapture()}//do poprawy
        PhongMaterial {
            id: material
            ambient: "gray"
            diffuse: "gray"
            specular: "black"
        }

        Entity {
            Mesh {
                id: modelMesh
                source: r_manager.modelChange
                onSourceChanged: doRenderCapture()
                onStatusChanged: {
                    doRenderCapture()
                    if(modelMesh.geometry == null)
                        return
                    //console.log(modelMesh.geometry)
                    _renderCaptureProvider.dawaj_model(modelMesh.geometry)
                }
            }

            Transform {
                id: modelTransform
                translation.x: r_manager.x
                translation.y: r_manager.z
                translation.z: -r_manager.y
                rotationX: r_manager.x_rot-90
                rotationY: r_manager.z_rot
                rotationZ: -r_manager.y_rot
                scale3D: Qt.vector3d(r_manager.x_scale,r_manager.y_scale,r_manager.z_scale)
                //PropertyChanges {
                    //target: qmlNote
                  //  onNoteChanged: doRenderCapture
                //}
                onScale3DChanged: doRenderCapture()
                onRotationXChanged: doRenderCapture()
                onTranslationChanged: doRenderCapture()

            }
            components: [modelMesh, material, modelTransform/*, screenRayCaster, mouseHandler*/]
        }

        Entity {
            PhongMaterial {
                id: mat
                diffuse: "red"
            }
            CylinderMesh {
                id: mod
                length: 30
                radius: 30
                slices: 3

            }
            Transform {
                id: tran
                translation.x: 100
                translation.y: 0
                translation.z: -100
            }
            components: move ? [mod, mat, tran] : []
            /*Component.onCompleted: {
                mod.geometry.positionAttribute.buffer.setSyncData(true)
                var vertexArray = new Float32Array(100);
                //console.log(mod.geometry.positionAttribute.byteStride)
                mod.geometry.positionAttribute.buffer.setUsage(Buffer.StreamRead)
                mod.geometry.positionAttribute.buffer.setAccessType(Buffer.Read)
                if(mod.geometry.positionAttribute.buffer.type == Buffer.VertexBuffer)
                    var triCount = mod.geometry.positionAttribute.byteStride
                    console.log(triCount)


                console.log(mod.geometry.positionAttribute.buffer.data().detach())
            }*/
        }

        GridEntity {
            id: raydisplay
            sizeX: window_manager.xBed
            sizeY: window_manager.yBed
        }
        AxisEntity {
            length: 20
        }
        LightEntity{}

    } // sceneRoot
}
