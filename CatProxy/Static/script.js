const urlbar = document.getElementById("urlbar");
const iframe = document.getElementById("browser");

urlbar.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        let url = urlbar.value;
        iframe.src = "/CatProxy/" + url;
    }
});