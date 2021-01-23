import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

Entity{
DirectionalLight {
    id: directional
    worldDirection: Qt.vector3d(0.0, 0.0, -1.0).normalized();
    color: "#fff2a3"
    intensity: 1
}
DirectionalLight {
    id: directional2
    worldDirection: Qt.vector3d(0.0, 0.0, 1.0).normalized();
    color: "#fff2a3"
    intensity: 1
}
DirectionalLight {
    id: directional3
    worldDirection: Qt.vector3d(0.0, -1.0, 0.0).normalized();
    color: "#fff2a3"
    intensity: 1.2
}
DirectionalLight {
    id: directional4
    worldDirection: Qt.vector3d(-1.0, 0.0, 0.0).normalized();
    color: "#fff2a3"
    intensity: .8
}
DirectionalLight {
    id: directional5
    worldDirection: Qt.vector3d(1.0, 0.0, 0.0).normalized();
    color: "#fff2a3"
    intensity: .8
}
components: [directional, directional2, directional3, directional4, directional5]
}
