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
    property var copy
    property var copyY
    property real linearSpeed: 0.5
    property bool visible: false
    property vector3d absolutePosition: Qt.vector3d(0, 0, 0)
    property real hoverHilightFactor: 1.44
    property var hoverElements: new Set()
    property var hoverElement: TransformGizmo.UIElement.None
    property var activeElement: TransformGizmo.UIElement.None
    components: [ownTransform, layer]

    enum UIElement {
        None,
        BeamX,
        BeamY,
        BeamZ
    }

    function deepCopy(p, c) {
        var c = c || {};
        for (var i in p) {
            if (typeof p[i] === 'object') {
                c[i] = (p[i].constructor === Array) ? [] : {};
                deepCopy(p[i], c[i]);
            } else {
                c[i] = p[i];
            }
        }
        return c;
    }
    // called by ObjectPickers of individual UI elements:
    function trackUIElement(element, active) {
        if(active) hoverElements.add(element)
        else hoverElements.delete(element)

        var newHoverElement = TransformGizmo.UIElement.None
        for(var x of [TransformGizmo.UIElement.BeamX, TransformGizmo.UIElement.BeamY, TransformGizmo.UIElement.BeamZ])
            if(newHoverElement === TransformGizmo.UIElement.None && hoverElements.has(x))
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
            visible = true
    }

    function detach() {
        //targetTransform.translation.x = r_manager.x
        //targetTransform.translation.y = r_manager.z
        //targetTransform.translation.z = -r_manager.y
        //targetTransform = null
        visible = false
        //targetTransform.matrix = Qt.matrix4x4(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)
        updateAbsolutePosition()
    }
    
    function translate(dx, dy, dz) {
        if(!targetTransform) return
        copy = targetTransform.translation.x
        copy += linearSpeed * dx
        r_manager.set_x(copy)
        copyY = -targetTransform.translation.z
        copyY += linearSpeed * dy
        r_manager.set_y(copyY)
        //targetTransform.translation.x += linearSpeed * dx
        //targetTransform.translation.y += linearSpeed * dy
        //targetTransform.translation.z += linearSpeed * dz
    }

    function save_translate(){
        //r_manager.set_x(copy)
        //targetTransform.translation.x = r_manager.x
        //r_manager.set_y(targetTransform.translation.z)
        //r_manager.set_z(-targetTransform.translation.y)
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
                if(hoverElement === TransformGizmo.UIElement.None) return
                lastPos = Qt.point(mouse.x, mouse.y)
                if(cameraController) cameraController.enabled = false
                activeElement = hoverElement
                return
            }
        }
        onPositionChanged: {
            if(activeElement === TransformGizmo.UIElement.None) return
            var dx = mouse.x - lastPos.x
            var dy = mouse.y - lastPos.y
            var d = projectMotion(dx, -dy)
            var x = activeElement === TransformGizmo.UIElement.BeamX
            var y = activeElement === TransformGizmo.UIElement.BeamY
            var z = activeElement === TransformGizmo.UIElement.BeamZ
            translate(x * d.x, y * d.y, z * d.z)
            
            lastPos = Qt.point(mouse.x, mouse.y)
        }
        onReleased: {
            if(activeElement === TransformGizmo.UIElement.None) return
            if(cameraController) cameraController.enabled = true
            activeElement = TransformGizmo.UIElement.None
            save_translate()
        }
    }



    NodeInstantiator {
        id: beams
        model: [
            {r: Qt.vector3d( 0, 0, -90), v: Qt.vector3d(1, 0, 0), color: "#f33", element: TransformGizmo.UIElement.BeamX},
            {r: Qt.vector3d( 0, 0,   0), v: Qt.vector3d(0, 1, 0), color: "#3f3", element: TransformGizmo.UIElement.BeamY},
            {r: Qt.vector3d(90, 0,   0), v: Qt.vector3d(0, 0, 1), color: "#33f", element: TransformGizmo.UIElement.BeamZ}
        ]
        delegate: Entity {
            components: [beamTransform]

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
                readonly property bool hilighted: active || (root.activeElement === TransformGizmo.UIElement.None && hover)
                readonly property color color: modelData.color
                components: [beamPicker]

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
                    components: [lineMesh, lineTransform, beamMaterial]

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
                    components: [translateMesh, translateTransform, beamMaterial]

                    ConeMesh {
                        id: translateMesh
                        enabled: root.visible
                        bottomRadius: 0.125 * absolutePosition.minus(camera.position).length() * 0.035 * 2
                        topRadius: 0
                        length: 0.125 * absolutePosition.minus(camera.position).length() * 0.2
                    }

                    Transform {
                        id: translateTransform
                        translation: Qt.vector3d(0, lineMesh.length + translateMesh.length / 2, 0)
                    }
                }

            }
        }
    }
}