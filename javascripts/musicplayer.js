function getSC() {
    var musicplayerElement = document.querySelector("iframe.soundcloud");
    if (musicplayerElement == null) {
        return null;
    }
    return SC.Widget(musicplayerElement);
}

async function musicplayerOnLoad() {

    // Private class for storing nonlocal static variables of music player
    class MusicPlayerStaticVariables {
        constructor(sc_widget) {
            this.sc = sc_widget;
            this.playlistLength = 1;
            this.isPlaying = false;
            this.ok_move = false;
        }

        updateByGetters() {
            this.ok_move = false;
            this.sc.getSounds((sounds) => {
                this.playlistLength = sounds.length;
                this.sc.isPaused((paused) => {
                    this.isPlaying = !paused;
                    this.ok_move = true;
                })
            });
        }
    };

    // Private function returning random integer in range [a, b)
    function randomInt(a, b) {
        return Math.floor(Math.random() * (b - a)) + a;
    }

    // Private function waiting for condition to be true
    async function whileWaiting(condition_callback, action_callback, timeout=200) {
        while (!condition_callback()) {
            await new Promise(resolve => setTimeout(resolve, timeout));
            if (action_callback != null) action_callback();
        }
    }

    var widget = getSC();
    await whileWaiting(() => (widget != null), () => { widget = getSC(); });
    var controller_button = document.querySelector("header.md-header .music-player.mcdic");
    var musicState = new MusicPlayerStaticVariables(widget);
    playButtonMode();

    function playButtonMode() {
        controller_button.classList.remove("pause-button");
        controller_button.classList.add("play-button");
        controller_button.title = "Play random music";
    }

    function stopButtonMode() {
        controller_button.classList.remove("play-button");
        controller_button.classList.add("pause-button");
        controller_button.title = "Stop this music";
    }

    async function togglePlay() {
        musicState.updateByGetters();
        await whileWaiting(() => musicState.ok_move, null);
        if (musicState.isPlaying) {
            widget.pause();
            playButtonMode();
        } else {
            widget.skip(randomInt(0, musicState.playlistLength));
            widget.seekTo(0);
            widget.setVolume(25);
            widget.play();
            stopButtonMode();
        }
    }
    controller_button.addEventListener("click", () => togglePlay().then(null));
}

musicplayerOnLoad().then(null);
