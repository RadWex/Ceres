import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

Entity {
    id: root
    property Layer layer
    property int sizeX : 200
    property int sizeY : 200
    //property int length: 1

    components: [ mesh, material, layer]

    property var ver_count: 0
    function buildVertexBufferData(size_x, size_y) {
        // Vertices
        var spacing = 10
        var ammountOfLinesX = size_x/spacing + 1;
        var ammountOfLinesY = size_y/spacing + 1;

        var vertexArray = new Float32Array((3 * ammountOfLinesX * 2) + (3 * ammountOfLinesY * 2)+6);
        //console.log(vertexArray.length)
        ver_count = vertexArray.length
        var j = 0;

        for (var i = 0; i < ammountOfLinesX -1 ; i++){

            vertexArray[j++] = spacing*i;
            vertexArray[j++] = 0;
            vertexArray[j++] = 0;
            vertexArray[j++] = spacing*i;
            vertexArray[j++] = 0;
            vertexArray[j++] = -size_y;
        }

        vertexArray[j++] = size_x;
        vertexArray[j++] = 0;
        vertexArray[j++] = 0;
        vertexArray[j++] = size_x;
        vertexArray[j++] = 0;
        vertexArray[j++] = -size_y;

        for (i = 0; i < ammountOfLinesY - 1; i++){
            vertexArray[j++] = 0;
            vertexArray[j++] = 0;
            vertexArray[j++] = -spacing*i;
            vertexArray[j++] = size_x;
            vertexArray[j++] = 0;
            vertexArray[j++] = -spacing*i;
        }
        vertexArray[j++] = 0;
        vertexArray[j++] = 0;
        vertexArray[j++] = -size_y;
        vertexArray[j++] = size_x;
        vertexArray[j++] = 0;
        vertexArray[j++] = -size_y;


        //console.log(vertexArray);
        return vertexArray;
    }

    Buffer {
        id: vertexBuffer
        type: Buffer.VertexBuffer
        data: buildVertexBufferData(root.sizeX, root.sizeY)
    }

    GeometryRenderer {
        id: mesh
        instanceCount: 1
        indexOffset: 0
        firstInstance: 0
        primitiveType: GeometryRenderer.Lines

        geometry:  Geometry {
            Attribute {
                attributeType: Attribute.VertexAttribute
                vertexBaseType: Attribute.Float
                vertexSize: 3
                byteOffset: 0
                count: ver_count
                name: defaultPositionAttributeName
                buffer: vertexBuffer
            }
        }
    }

    LineMaterial {
        id: material
        maincolor: "dimgray"
    }
}
