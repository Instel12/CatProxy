function Wipe() {
    if (confirm("You sure?")) {
        localStorage.clear();
    }
}

function Dump() {
    const json = JSON.stringify(localStorage, null, 4);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "CatStorageDump.json";
    document.body.appendChild(a);
    a.click();
    a.remove();

    URL.revokeObjectURL(url);
}

function Load() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json,application/json";

    input.onchange = () => {
        const file = input.files[0];
        const reader = new FileReader();

        reader.onload = () => {
            try {
                const data = JSON.parse(reader.result);

                for (const [key, value] of Object.entries(data)) {
                    localStorage.setItem(key, value);
                }

                alert("Loaded!");
            } catch {
                alert("Invalid file");
            }
        };
        reader.readAsText(file);
    };
    input.click();
}