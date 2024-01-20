function autoscrollGetY() {
    const scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
    const scrollHeight = document.body.scrollHeight || document.documentElement.scrollHeight;
    return {
        "top": scrollTop,
        "height": scrollHeight,
        "needMoveDown": (scrollTop < 0.8 * scrollHeight)
    };
}

function autoscrollUpdateTitle(element) {
    const Y = autoscrollGetY();
    if(Y.needMoveDown) {
        element.title = "Move to the bottom";
    }
    else {
        element.title = "Move to the top";
    }
}

function autoscrollMove() {
    const Y = autoscrollGetY();
    if(Y.needMoveDown) {
        window.scrollTo({"top": Y.height, "left": 0, "behavior": "smooth"});
    }
    else {
        window.scrollTo({"top": 0, "left": 0, "behavior": "smooth"});
    }
}

function autoscrollOnClick() {
    autoscrollMove();
}

function autoscrollOnLoad(element) {
    autoscrollUpdateTitle(element);
    function autoscrollEvent(event) {
        autoscrollUpdateTitle(element);
    }
    addEventListener("scroll", autoscrollEvent);
}

autoscrollOnLoad(document.getElementsByClassName("mcdic auto-scroller")[0]);
