/*
qt3d-transform-gizmo
Copyright (C) 2020  Federico Ferri
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick.Scene3D 2.0
import QtQuick 2.2 as QQ2
import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Logic 2.0
import Qt3D.Extras 2.0
import Qt3D.Animation 2.9

Entity {
    id: root
    property bool is_active: true
    property Layer layer
    property var cameraController
    property Camera camera
    property Transform targetTransform
    property bool visible: false
    property vector3d absolutePosition: Qt.vector3d(0, 0, 0)
    property real hoverHilightFactor: 1.44
    property real angularSpeed: 2.0
    property var hoverElements: new Set()
    property var hoverElement: RotationGizmo.UIElement.None
    property var activeElement: RotationGizmo.UIElement.None
    components: [ownTransform, layer]

    enum UIElement {
        None,
        BeamX,
        BeamY,
        BeamZ
    }

    // called by ObjectPickers of individual UI elements:
    function trackUIElement(element, active) {
        if(active) hoverElements.add(element)
        else hoverElements.delete(element)

        var newHoverElement = RotationGizmo.UIElement.None
        for(var x of [RotationGizmo.UIElement.BeamX, RotationGizmo.UIElement.BeamY, RotationGizmo.UIElement.BeamZ])
            if(newHoverElement === RotationGizmo.UIElement.None && hoverElements.has(x))
                newHoverElement = x
        hoverElement = newHoverElement
    }

    function getMatrix(entity) {
        var t = getTransform(entity)
        if(t) return t.matrix
        return Qt.matrix4x4(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)
    }

    function getAbsoluteMatrix() {
        var entity = root
        var m = Qt.matrix4x4(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)
        while(entity) {
            m = getMatrix(entity).times(m)
            entity = entity.parent
        }
        return m
    }

    function project(v, modelView, projection, viewport) {
        // ported from qtbase/src/gui/math3d/qvector3d.cpp
        var tmp = Qt.vector4d(v.x, v.y, v.z, 1)
        tmp = projection.times(modelView).times(tmp)
        if(Math.abs(tmp.z) < 0.00001)
            tmp.z = 1
        tmp = tmp.times(1 / tmp.w)

        tmp = tmp.times(0.5).plus(Qt.vector4d(0.5, 0.5, 0.5, 0.5))
        tmp.x = tmp.x * viewport.width + viewport.x
        tmp.y = tmp.y * viewport.height + viewport.y
        return Qt.vector3d(tmp.x, tmp.y, tmp.z)
    }

    function projectMotion(dx, dy) {
        var mtx = getAbsoluteMatrix()
        var mv = camera.viewMatrix.times(mtx)
        var p = camera.projectionMatrix
        var v = Qt.rect(0, 0, scene3d.width, scene3d.height)

        var s0 = project(Qt.vector3d(0,0,0),mv,p,v)
        var sx = project(Qt.vector3d(1,0,0),mv,p,v).minus(s0)
        var sy = project(Qt.vector3d(0,1,0),mv,p,v).minus(s0)
        var sz = project(Qt.vector3d(0,0,1),mv,p,v).minus(s0)
        sx.z = sy.z = sz.z = 0
        sx = sx.normalized()
        sy = sy.normalized()
        sz = sz.normalized()

        var d = Qt.vector3d(dx, dy, 0)
        var px = d.dotProduct(sx)
        var py = d.dotProduct(sy)
        var pz = d.dotProduct(sz)
        return Qt.vector3d(px, py, pz)
    }

    function updateAbsolutePosition() {
        // compute absolute position to expose as a property
        var m = getAbsoluteMatrix()
        absolutePosition = Qt.vector3d(m.m14, m.m24, m.m34)
    }

    function qmlInstanceOf(obj, className) {
        return obj.toString().indexOf(className + "(") === 0;
    }

    function getTransform(entity) {
        if(entity instanceof Entity)
            for(var i = 0; i < entity.components.length; i++)
                if(qmlInstanceOf(entity.components[i], "Qt3DCore::QTransform"))
                    return entity.components[i]
    }

    function attachTo(entity) {
            targetTransform = getTransform(entity)
            fixOwnTransform()
            visible = true
    }

    function detach() {
        visible = false
        targetTransform = null
        updateAbsolutePosition()
    }

    function fixOwnTransform() {
        // cancel rotation component of parent's (target) transform
        var t = targetTransform.matrix
        var i = t.inverted()
        i = i.times(Qt.matrix4x4(1,0,0,t.m14+r_manager.origin.x,
                                 0,0,1,t.m24+r_manager.origin.z,
                                 0,-1,0,t.m34-r_manager.origin.y,
                                 0,0,0,1))
        ownTransform.matrix = i

        updateAbsolutePosition()
    }

    function rotate(dx, dy, dz) {
        if(!targetTransform) return
        var t = targetTransform.matrix

        var x = Math.atan2(t.m32, t.m33) * (180/Math.PI) + 90
        x += angularSpeed * dx 
        r_manager.set_x_rot(x)

        var y = Math.atan2(t.m21, t.m11) * (180/Math.PI)
        y += angularSpeed * dy
        r_manager.set_y_rot(y)

        var z = Math.atan2(-t.m31, Math.sqrt(t.m32*t.m32+t.m33*t.m33)) * (180/Math.PI)
        z += angularSpeed * dz
        r_manager.set_z_rot(z)
    }

    QQ2.Loader {
        active: !!targetTransform
        sourceComponent: QQ2.Connections {
            target: targetTransform
            onMatrixChanged: fixOwnTransform()
        }
    }

    Transform {
        id: ownTransform
    }

    MouseDevice {
        id: mouseDev
    }

    MouseHandler {
        sourceDevice: mouseDev
        property point lastPos
        onPressed: {
            if(is_active == false) {
                detach()
                return
            }
            if(mouse.button == Qt.LeftButton) {
                if(hoverElement === RotationGizmo.UIElement.None) return
                lastPos = Qt.point(mouse.x, mouse.y)
                if(cameraController) cameraController.enabled = false
                activeElement = hoverElement
                return
            }
        }
        onPositionChanged: {
            if(activeElement === RotationGizmo.UIElement.None) return
            var dx = mouse.x - lastPos.x
            var dy = mouse.y - lastPos.y
            var d = projectMotion(dx, -dy)
            var x = activeElement === RotationGizmo.UIElement.BeamX
            var y = activeElement === RotationGizmo.UIElement.BeamY
            var z = activeElement === RotationGizmo.UIElement.BeamZ
            rotate(x * d.x, y * d.y, z * d.z)
            
            lastPos = Qt.point(mouse.x, mouse.y)
        }
        onReleased: {
            if(activeElement === RotationGizmo.UIElement.None) return
            if(cameraController) cameraController.enabled = true
            activeElement = RotationGizmo.UIElement.None
        }
    }

    NodeInstantiator {
        id: beams
        model: [
            {r: Qt.vector3d( 0, 0, -90), v: Qt.vector3d(1, 0, 0), color: "#f33", element: RotationGizmo.UIElement.BeamX},
            {r: Qt.vector3d( 0, 0,   0), v: Qt.vector3d(0, 1, 0), color: "#3f3", element: RotationGizmo.UIElement.BeamY},
            {r: Qt.vector3d(90, 0,   0), v: Qt.vector3d(0, 0, 1), color: "#33f", element: RotationGizmo.UIElement.BeamZ}
        ]
        delegate: Entity {
            components: visible ? [beamTransform] : []

            Transform {
                id: beamTransform
                
                rotationX: modelData.r.x
                rotationY: modelData.r.y
                rotationZ: modelData.r.z
            }

            Entity {
                id: beam
                readonly property bool hover: root.hoverElement === modelData.element
                readonly property bool active: root.activeElement === modelData.element
                readonly property bool hilighted: active || (root.activeElement === RotationGizmo.UIElement.None && hover)
                readonly property color color: modelData.color
                components: visible ? [beamPicker] : []

                ObjectPicker {
                    id: beamPicker
                    hoverEnabled: true
                    onEntered: root.trackUIElement(modelData.element, true)
                    onExited: root.trackUIElement(modelData.element, false)
                }

                PhongMaterial {
                    id: beamMaterial
                    ambient: beam.hilighted ? Qt.lighter(beam.color, root.hoverHilightFactor) : beam.color
                }

                Entity {
                    components: visible ? [lineMesh, lineTransform, beamMaterial] : []

                    CylinderMesh {
                        id: lineMesh
                        enabled: root.visible
                        radius: 0.125 * absolutePosition.minus(camera.position).length() *  0.035
                        length: 0.125 * absolutePosition.minus(camera.position).length() * 0.8
                    }

                    Transform {
                        id: lineTransform
                        translation: Qt.vector3d(0, lineMesh.length / 2, 0)
                    }
                }

                Entity {
                    components: visible ? [rotateMesh, rotateTransform, beamMaterial] : []

                    CylinderMesh {
                        id: rotateMesh
                        enabled: root.visible
                        radius: 0.125 * absolutePosition.minus(camera.position).length() * 0.035 * 2
                        length: 0.125 * absolutePosition.minus(camera.position).length() * 0.2
                    }

                    Transform {
                        id: rotateTransform
                        translation: Qt.vector3d(0, lineMesh.length + rotateMesh.length / 2, 0)
                    }
                }

            }
        }
    }
}