import QtQuick 2.2
import Qt3D.Core 2.0
import Qt3D.Render 2.15
import Qt3D.Input 2.0
import Qt3D.Extras 2.15

Entity{
    id: root
    property int length : 20

    PhongMaterial {
        id: materialX
        diffuse: "red"
        specular: "black"
    }

    Entity {
        CylinderMesh {
            id: cylinderX
            length: root.length
            radius: .5
        }
        Transform {
            id: cylinderTransformX
            translation.x: root.length/2
            translation.y: 0
            translation.z: 0
            rotationZ: -90
        }
        components: [cylinderX, materialX, cylinderTransformX]
    }

    Entity {
        ConeMesh {
            id: coneX
            length: root.length/3
            bottomRadius: root.length/15
            topRadius: 0
        }
        Transform {
            id: coneTransformX
            translation.x: root.length + root.length/6
            translation.y: 0
            translation.z: 0
            rotationZ: -90
        }
        components: [coneX, materialX, coneTransformX]
    }

    PhongMaterial {
        id: materialY
        diffuse: "green"
        specular: "black"
    }

    Entity {
        CylinderMesh {
            id: cylinderY
            length: root.length
            radius: .5
        }
        Transform {
            id: cylinderTransformY
            translation.x: 0
            translation.y: 0
            translation.z: -root.length/2
            rotationX: -90
        }
        components: [cylinderY, materialY, cylinderTransformY]
    }

    Entity {
        ConeMesh {
            id: coneY
            length: root.length/3
            bottomRadius: root.length/15
            topRadius: 0
        }
        Transform {
            id: coneTransformY
            translation.x: 0
            translation.y: 0
            translation.z: -root.length - root.length/6
            rotationX: -90
        }
        components: [coneY, materialY, coneTransformY]
    }

    PhongMaterial {
        id: materialZ
        diffuse: "blue"
        specular: "black"
    }

    Entity {
        CylinderMesh {
            id: cylinderZ
            length: root.length
            radius: .5
        }
        Transform {
            id: cylinderTransformZ
            translation.x: 0
            translation.y: root.length/2
            translation.z: 0
            //rotationX: -90
        }
        components: [cylinderZ, materialZ, cylinderTransformZ]
    }

    Entity {
        ConeMesh {
            id: coneZ
            length: root.length/3
            bottomRadius: root.length/15
            topRadius: 0
        }
        Transform {
            id: coneTransformZ
            translation.x: 0
            translation.y: root.length + root.length/6
            translation.z: 0
        }
        components: [coneZ, materialZ, coneTransformZ]
    }
}
