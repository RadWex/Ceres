import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

Entity {
    id: root

    property int sizeX
    property int sizeY
    //property int length: 1

    components: [ mesh, material ]

    property var ver_count: 0
    function buildVertexBufferData(size_x, size_y) {
        // Vertices
        var spacing = 10
        var ammountOfLinesX = size_x/spacing + 1;
        var ammountOfLinesY = size_y/spacing + 1;
        //var v1 = o.plus(d.times(l));
        //ver_count = size_x * 2 + size_y * 2;
        var vertexArray = new Float32Array((3 * ammountOfLinesX * 2) + (3 * ammountOfLinesY * 2));
        ver_count = vertexArray.length
        var j = 0;
        for (var i = 0; i < ammountOfLinesX; i++){

            vertexArray[j++] = spacing*i;
            vertexArray[j++] = 0;
            vertexArray[j++] = 0;
            vertexArray[j++] = spacing*i;
            vertexArray[j++] = size_y;
            vertexArray[j++] = 0;
        }
        for (i = 0; i < ammountOfLinesY; i++){
            vertexArray[j++] = 0;
            vertexArray[j++] = spacing*i;
            vertexArray[j++] = 0;
                        vertexArray[j++] = size_x;
            vertexArray[j++] = spacing*i;

            vertexArray[j++] = 0;
        }

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
