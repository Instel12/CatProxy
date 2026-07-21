// this is rlly bad but at least i tried

window.onload = () => {
    function removeAds() {
        document.querySelectorAll("[data-ad]").forEach(ad => {
            ad.remove();
        });

        document.querySelectorAll("ins").forEach(ad => {
            if (
                ad.id.startsWith("gpt_unit_") ||
                ad.id.includes("/INTER-")
            ) {
                ad.remove();
            }
        });
    }

    removeAds();

    const observer = new MutationObserver(() => {
        removeAds();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
};