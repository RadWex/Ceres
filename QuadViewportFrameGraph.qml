import QtQuick 2.2
import Qt3D.Core 2.0
import Qt3D.Render 2.1
import Qt3D.Input 2.0
import Qt3D.Extras 2.0


RenderSettings {
    id: quadViewportFrameGraph
    property alias topLeftCamera: cameraSelectorTopLeftViewport.camera;
    property alias bottomRightCamera: cameraSelectorBottomRightViewport.camera;
    property alias window: surfaceSelector.surface
    property var renCap: renderCapture

    activeFrameGraph: RenderSurfaceSelector {
        id: surfaceSelector
        ClearBuffers {
            buffers: ClearBuffers.ColorDepthBuffer
            clearColor: Qt.rgba(0.6, 0.6, 0.6, 1.0)
            Viewport {
                id: topLeftViewport
                CameraSelector{
                    id: cameraSelectorTopLeftViewport
                    RenderCapture {
                        id:renderCapture
                    }
                }
            }
        }

        ClearBuffers {
            buffers: ClearBuffers.ColorDepthBuffer
            clearColor: Qt.rgba(0.6, 0.6, 0.6, 1.0)
            NoDraw {}
            CameraSelector{
                id: cameraSelectorBottomRightViewport
            }
        }
    }
}
