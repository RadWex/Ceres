import Qt3D.Core 2.0
import Qt3D.Render 2.0

Material {
    id: root

    //! [0]
    property color maincolor: Qt.rgba(0.0, 0.0, 0.0, 1.0)

    parameters: [
        Parameter {
            name: "maincolor"
            value: Qt.vector3d(root.maincolor.r, root.maincolor.g, root.maincolor.b)
        }
    ]

    //! [0]

    effect: Effect {

        //! [1]
        property string vertex: "shaders/gl3/simpleColor.vert"
        property string fragment: "shaders/gl3/simpleColor.frag"
        //property string vertexES: "qrc:/shaders/es2/simpleColor.vert"
        //property string fragmentES: "qrc:/shaders/es2/simpleColor.frag"
        //! [1]

        FilterKey {
            id: forward
            name: "renderingStyle"
            value: "forward"
        }

        //! [2]
        ShaderProgram {
            id: gl3Shader
            vertexShaderCode: loadSource(Qt.resolvedUrl("../shaders/simpleColor.vert"))
            fragmentShaderCode: loadSource(Qt.resolvedUrl("../shaders/simpleColor.frag"))
        }

        //! [2]

        techniques: [
            //! [3]
            // OpenGL 3.1
            Technique {
                filterKeys: [forward]
                graphicsApiFilter {
                    api: GraphicsApiFilter.OpenGL
                    profile: GraphicsApiFilter.CoreProfile
                    majorVersion: 3
                    minorVersion: 1
                }
                renderPasses: RenderPass {
                    shaderProgram: gl3Shader
                }
            }


        ]
    }
}
