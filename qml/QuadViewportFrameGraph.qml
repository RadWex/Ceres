import QtQuick 2.2
import Qt3D.Core 2.0
import Qt3D.Render 2.1
import Qt3D.Input 2.0
import Qt3D.Extras 2.0


RenderSettings {
    id: quadViewportFrameGraph
    property alias topLeftCamera: cameraSelectorTopLeftViewport.camera;
    property alias bottomRightCamera: cameraSelectorBottomRightViewport.camera;
    property var renCap: renderCapture

    Viewport {
                        normalizedRect: Qt.rect(0.0, 0.0, 1.0, 1.0)
    RenderSurfaceSelector {
        CameraSelector{
            id: cameraSelectorTopLeftViewport
            FrustumCulling {
                ClearBuffers {
                    buffers: ClearBuffers.AllBuffers
                    clearColor: Qt.rgba(0.6, 0.6, 0.6, 1.0)
                    NoDraw {}
                }
                LayerFilter {
                    filterMode: LayerFilter.AcceptAnyMatchingLayers
                    layers: [modelLayer, lightLayer]
                    RenderCapture {
                        id:renderCapture
                    }
                }
            }
            
        }
        
        CameraSelector{
            id: cameraSelectorBottomRightViewport
            FrustumCulling {
                ClearBuffers {
                    buffers: ClearBuffers.AllBuffers
                    clearColor: Qt.rgba(0.6, 0.6, 0.6, 1.0)
                    NoDraw {}
                }
                LayerFilter {
                    filterMode: LayerFilter.DiscardAnyMatchingLayers
                    layers: [topLayer]
                }
                LayerFilter {
                    filterMode: LayerFilter.AcceptAnyMatchingLayers
                    layers: [topLayer]
                    ClearBuffers {
                        buffers: ClearBuffers.DepthBuffer
                    }
                }
            }
        }  
    }
    }
    pickingSettings.pickMethod: PickingSettings.TrianglePicking
    pickingSettings.pickResultMode: PickingSettings.AllPicks
    pickingSettings.faceOrientationPickingMode: PickingSettings.FrontAndBackFace
}
