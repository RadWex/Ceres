import QtQuick 2.2
import Qt3D.Core 2.0
import Qt3D.Render 2.15
import Qt3D.Input 2.0
import Qt3D.Extras 2.15


Entity {
    id: rootNode
    property bool move
    property bool rotate
    property var reply
    
    //button move event
    onMoveChanged: {
        if(move)
            tg.attachTo(model)
        else
            tg.detach()
    }

    //button rotate event
    onRotateChanged: {
        if(rotate)
            rotateGizmo.attachTo(model)
        else
            rotateGizmo.detach()
    }

    function doRenderCapture()
    {
        reply = scene.requestRenderCapture()
        reply.completed.connect(onRenderCaptureComplete)
    }

    function onRenderCaptureComplete()
    {
        _renderCaptureProvider.render(reply.image)
    }

    function requestRenderCapture()
    {
        return quadViewportFrameGraph.renCap.requestCapture()
    }

    components: [quadViewportFrameGraph, inputSettings, raycaster]

    QuadViewportFrameGraph {
        id: quadViewportFrameGraph
        topLeftCamera: cameraSet.cameras[0]
        bottomRightCamera: cameraSet.cameras[1]
    }

    InputSettings { id: inputSettings }

    Entity {
        id: cameraSet
        property var cameras: [virtual_camera, camera]

        Camera {
            id: camera
            projectionType: CameraLens.PerspectiveProjection
            fieldOfView: 30
            aspectRatio: 16 / 9
            nearPlane: 0.1
            farPlane: 2000.0
            position: cameraManager.position
            //upVector: Qt.vector3d(-100.0, 0.0, -100.0)
            viewCenter: cameraManager.view
            //onPositionChanged: { console.log(camera.viewMatrix)}
        }

        Camera {
            id: virtual_camera
            projectionType: CameraLens.OrthographicProjection

            nearPlane: 0.1
            farPlane: 1000.0
            left: -window_manager.xBed/2
            right: window_manager.xBed/2
            bottom: -window_manager.yBed/2
            top: window_manager.yBed/2
            position: Qt.vector3d(100.0, 100.0, -100.0)
            //upVector: Qt.vector3d(0.0, 1.0, 0.0)
            
            viewCenter: Qt.vector3d(100.0, 0.0, -100.0)
        }
    }

    SOrbitCameraController {
            id: mainCameraController
            camera: camera
    }

    Layer {
        id: topLayer
        recursive: true
    }

    
    function printHits(desc, hits) {
        console.log(desc, hits.length)
        for (var i=0; i<hits.length; i++) {
            console.log("  " + hits[i].entity.objectName, hits[i].distance,
                        hits[i].worldIntersection.x, hits[i].worldIntersection.y, hits[i].worldIntersection.z)
        }
    }
    /*
    RayCaster {
        id: raycaster
        origin: Qt.vector3d(100, 40, -100)
        direction: Qt.vector3d(0., -1., 0.)
        length: 100

        onHitsChanged: printHits("Model hits", hits)
    }

    LineEntity {
        origin: Qt.vector3d(100, 40, -100)
        direction: Qt.vector3d(0., -1., 0.)
        length: 100
    }
    */
    function set_on_bed(){
        r_manager.set_z(-r_manager.bottomLeftOrigin.z)
        //raycaster.trigger()
    }

    function center_on_bed(){
        r_manager.set_x(window_manager.xBed/2-r_manager.origin.x)
        r_manager.set_y(window_manager.yBed/2-r_manager.origin.y)
    }

    PhongMaterial {
        id: material
        ambient: "gray"
        diffuse: "gray"
        specular: "black"
    }

    Entity {
        id: model
        Layer {
            id: modelLayer
        }
        Mesh {
            id: modelMesh
            source: r_manager.modelChange
            onStatusChanged: {
                //raycaster.trigger()
                //if(modelMesh.geometry == null)
                //    return
                if(modelMesh.status == 2) {
                    _renderCaptureProvider.get_geometry(modelMesh.geometry)
                    console.log("--------new model--------")
                    console.log("central origin: "+r_manager.origin)
                    console.log("bottom left origin: "+r_manager.bottomLeftOrigin)
                }
            }
        }

        Transform {
            id: modelTransform
            matrix: r_manager.matrix
            onMatrixChanged: doRenderCapture()
        }

        TransformGizmo {
            id: tg
            layer: topLayer
            cameraController: mainCameraController
            camera: camera
            is_active: move
            //size: 0.125 * absolutePosition.minus(camera.position).length()
        }
        
        RotationGizmo {
            id: rotateGizmo
            layer: topLayer
            cameraController: mainCameraController
            camera: camera
            is_active: rotate
        }

        components: [modelMesh, material, modelTransform, modelLayer]
    }
    
    GridEntity {
        Layer {
            id: gridLayer
        }
        id: raydisplay
        sizeX: window_manager.xBed
        sizeY: window_manager.yBed
        layer: gridLayer
    }
    
    AxisEntity {
        length: 20
    }

    LightEntity {
        Layer {
            id: lightLayer
        }
        layer: lightLayer
    }

}
