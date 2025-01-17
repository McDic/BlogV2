const SC2 = SC;
console.log(SC2);

function musicplayerOnLoad() {
    var musicplayerElement = document.querySelector("iframe.soundcloud");
    if (musicplayerElement == null) {
        return;
    }
    var widget = SC.Widget(musicplayerElement);
}
