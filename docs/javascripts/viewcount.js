async function loadViewCache(path) {
    const response = await fetch("/assets/views.json");
    const jsonResult = await response.json();
    if(!jsonResult[path]) return undefined;
    else return jsonResult[path].total_users;
};

// https://stackoverflow.com/questions/9345136/1000000-to-1m-and-1000-to-1k-and-so-on-in-js
function formatKMGT(n,d){
    x=(''+n).length;
    p=Math.pow;
    d=p(10,d);
    x-=x%3;
    return Math.round(n*d/p(10,x))/d+" KMGTPE"[x/3];
};

async function loadCurrentPageView() {
    const metadata_views = document.getElementById("post-metadata-views");
    if(!metadata_views) return;
    const inner_metadata_views = metadata_views.getElementsByClassName("md-ellipsis")[0];
    const views = await loadViewCache(window.location.pathname);
    if(views !== 0 && !views) {
        metadata_views.style.display = "none";
    }
    else {
        metadata_views.style.display = "inherit";
        inner_metadata_views.textContent = formatKMGT(views, 2) + " users viewed";
    }
}
