///////////////////////
// manage Pages
///////////////////////

function getCurrentPageKey() {
    const bodyPage = document.body.dataset.page;
    if (bodyPage) {
        return bodyPage;
    }

    const path = window.location.pathname.replace("/", "") || "home";
    return path;
}

function setActiveNavigation() {
    const currentPage = getCurrentPageKey();

    document.querySelectorAll(".nav-item").forEach((item) => {
        const isActive = item.dataset.page === currentPage;
        item.classList.toggle("active", isActive);
    });
}

function bindNavigation() {
    document.querySelectorAll(".nav-item").forEach((item) => {
        item.addEventListener("click", () => {
            const target = item.dataset.page;
            const page = target === "home" ? "/" : "/" + target;
            window.location.href = page;
        });
    });
}

///////////////////////
// load data
///////////////////////

async function load_notes() {
    const input_text = document.getElementById("content");
    try {
        const response = await fetch("/notes_load");
        if (!response.ok) {
            throw new Error(`HTTP-Fehler! Status: ${response.status}`);
        }
        const result = await response.json();
        if (input_text) {
            input_text.value = result.data ?? "";
        }
    } catch (e) {
        if (input_text) {
            input_text.value = `[Fehler] ${e.message}`;
        }
    }
}

///////////////////////
// save data
///////////////////////

async function save_notes() {
    const input_text = document.getElementById("content");
    try {
        const payload = { content: input_text ? input_text.value : "" };
        const response = await fetch("/notes_save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP-Fehler! Status: ${response.status}`);
        }

        const result = await response.json();
        if (result.status === 0) {
            if (input_text) {
                input_text.value = payload.content;
            }
        }
    } catch (e) {
        if (input_text) {
            input_text.value = `[Fehler] ${e.message}`;
        }
    }
}

async function load_media_list() {
    const list = document.getElementById("media-list");
    try {
        const response = await fetch("/media_load");
        if (!response.ok) {
            throw new Error(`HTTP-Fehler! Status: ${response.status}`);
        }
        const result = await response.json();
        const files = result.data ?? [];

        if (!list) {
            return;
        }

        list.innerHTML = "";
        files.forEach((fileName) => {
            const item = document.createElement("li");
            item.textContent = fileName;
            list.appendChild(item);
        });
    } catch (e) {
        if (list) {
            list.innerHTML = `<li>[Fehler] ${e.message}</li>`;
        }
    }
}

async function upload_media() {
    const fileInput = document.getElementById("media-file");
    const list = document.getElementById("media-list");

    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        if (list) {
            list.innerHTML = "<li>Bitte Datei auswählen.</li>";
        }
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/media_add", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP-Fehler! Status: ${response.status}`);
        }

        const result = await response.text();
        if (result === "1") {
            fileInput.value = "";
            await load_media_list();
        } else {
            if (list) {
                list.innerHTML = "<li>Upload fehlgeschlagen.</li>";
            }
        }
    } catch (e) {
        if (list) {
            list.innerHTML = `<li>[Fehler] ${e.message}</li>`;
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    bindNavigation();
    setActiveNavigation();

    const saveButton = document.getElementById("save-notes");
    if (saveButton) {
        saveButton.addEventListener("click", save_notes);
    }

    const loadButton = document.getElementById("load-notes");
    if (loadButton) {
        loadButton.addEventListener("click", load_notes);
    }

    const uploadButton = document.getElementById("media-upload");
    if (uploadButton) {
        uploadButton.addEventListener("click", upload_media);
    }

    if (document.getElementById("content")) {
        load_notes();
    }

    if (document.getElementById("media-list")) {
        load_media_list();
    }
});
