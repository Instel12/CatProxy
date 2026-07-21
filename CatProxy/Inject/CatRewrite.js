(() => {
    const routeName = (window.CatProxyRoute || "CatProxy").replace(/^\/+|\/+$/g, "");
    const proxyRoute = `/${routeName}/`;
    const originalBase = window.CatProxyBase || window.location.href;

    function shouldIgnore(url) {
        if (!url) {
            return true;
        }

        const value = String(url).trim();

        return (
            !value ||
            value.startsWith("data:") ||
            value.startsWith("blob:") ||
            value.startsWith("javascript:") ||
            value.startsWith("mailto:") ||
            value.startsWith("tel:") ||
            value.startsWith("#") ||
            value.startsWith("about:") ||
            value.startsWith("file:") ||
            value.includes("/Inject/") ||
            value.startsWith(proxyRoute) ||
            value.startsWith(window.location.origin + proxyRoute)
        );
    }

    function rewriteURL(url) {
        if (shouldIgnore(url)) {
            return url;
        }

        let resolved = url;

        try {
            resolved = new URL(url, originalBase).href;
        } catch {
            return url;
        }

        if (resolved.startsWith(window.location.origin + proxyRoute)) {
            return resolved;
        }

        if (resolved.startsWith(window.location.origin)) {
            try {
                const current = new URL(resolved);
                const original = new URL(originalBase);

                resolved = original.origin + current.pathname + current.search + current.hash;
            } catch {}
        }

        return proxyRoute + resolved;
    }

    function rewriteSrcset(value) {
        if (!value) {
            return value;
        }

        return value
            .split(",")
            .map(entry => {
                const trimmed = entry.trim();
                if (!trimmed) {
                    return entry;
                }

                const parts = trimmed.split(/\s+(?=\S+$)/);
                const candidate = parts[0];
                const descriptor = parts.slice(1).join(" ");
                const rewritten = rewriteURL(candidate);

                return descriptor ? `${rewritten} ${descriptor}` : rewritten;
            })
            .join(", ");
    }

    function rewriteElements(root = document) {
        root.querySelectorAll("[src], [href], [action], [poster], [srcset], [data-src], [data-href], [data-srcset]").forEach(element => {
            const attributes = ["src", "href", "action", "poster", "srcset", "data-src", "data-href", "data-srcset"];

            attributes.forEach(attr => {
                const value = element.getAttribute(attr);

                if (!value) {
                    return;
                }

                const rewritten = attr === "srcset" || attr === "data-srcset"
                    ? rewriteSrcset(value)
                    : rewriteURL(value);

                if (rewritten !== value) {
                    element.setAttribute(attr, rewritten);
                }
            });
        });
    }

    rewriteElements();

    new MutationObserver(() => {
        rewriteElements();
    }).observe(document.documentElement, {
        childList: true,
        subtree: true
    });

    const oldFetch = window.fetch;

    window.fetch = function(input, options) {
        if (typeof input === "string") {
            input = rewriteURL(input);
        }
        else if (input instanceof Request) {
            input = new Request(rewriteURL(input.url), input);
        }

        return oldFetch.call(this, input, options);
    };

    const oldOpen = XMLHttpRequest.prototype.open;

    XMLHttpRequest.prototype.open = function(method, url, ...args) {
        return oldOpen.call(this, method, rewriteURL(url), ...args);
    };

    console.log("[CatProxy] Rewriter loaded");
})();
