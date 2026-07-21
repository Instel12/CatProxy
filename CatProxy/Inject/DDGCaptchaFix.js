// this is just a temp thing so that you can actually search stuff up

function check(){
    var catchas = document.getElementsByClassName("anomaly-modal__image");

    Array.from(catchas).forEach(element => {
        let style = element.getAttribute("style");
        if (!style.includes(location.origin)) style = style.replace("background-image: url('", `background-image: url('${location.origin}/${window.CatProxyRoute}/duckduckgo.com/`);
        element.setAttribute("style", style);
    });

    setTimeout(check, 500);
}

check();