import QtQuick 2.15
import "content"

Rectangle {
    width: 500; height: 700
    color: "#464646"

    ListModel {
        id: list

        ListElement {
            name: "Panel One"
            notes: [
                ListElement { noteText: "Tap to edit" },
                ListElement { noteText: "Drag to move" },
                ListElement { noteText: "Flick to scroll" },
                ListElement { noteText: "Swipe to next panel" }
            ]
        }

        ListElement {
            name: "Panel Two"
            notes: [
                ListElement { noteText: "To open the doors, just click them" },
                ListElement { noteText: "We have one more panel" }

            ]
        }

        ListElement {
            name: "Panel Three"
            notes: [
                ListElement { noteText: "You can close them by re-clicking" }
            ]
        }
    }

    ListView {
        id: flickable

        anchors.fill: parent
        focus: true
        highlightRangeMode: ListView.StrictlyEnforceRange
        orientation: ListView.Horizontal
        snapMode: ListView.SnapOneItem
        model: list
        delegate: Panel { }
    }
}
