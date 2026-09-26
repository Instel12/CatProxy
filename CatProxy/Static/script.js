const urlbar = document.getElementById("urlbar");
const iframe = document.getElementById("browser");
const favicon = document.getElementById("favicon");

function isURL(string){
    if (string.startsWith("cat://")){
        return true;
    }
    
    try{
        new URL(string);
        return true;
    }
    catch{
        return false;
    }
}

urlbar.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        let url = urlbar.value;
        if (isURL(url)){
            iframe.src = "/CatProxy/" + url;
        }
        else{
            iframe.src = "/CatProxy/https://duckduckgo.com/?q=" + url;
        }
    }
});

iframe.addEventListener("load", function() {
    try {
        urlbar.value = iframe.contentWindow.location.href.replace(location.origin + "/CatProxy/", "");
    } catch {
    }

    try {
        favicon.src = getFavicon();
        favicon.style.display = favicon.src ? "inline" : "none";
    }
    catch {
        favicon.style.display = "none";
    }
    
    favicon.onerror = () => {
        favicon.style.display = "none";
    };
});

function getFavicon() {
    try {
        const doc = iframe.contentDocument;
        const icon = doc.querySelector('link[rel~="icon"]');

        try {
            return icon.href;
        }
        catch{
                return new URL("/favicon.ico", iframe.contentWindow.location.href).href;
        }
    } catch (error) {
        return null;
    }
}