const urlbar = document.getElementById("urlbar");
const iframe = document.getElementById("browser");

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