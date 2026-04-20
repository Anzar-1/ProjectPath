const receivedTab = document.getElementById("receivedTab");
const sentTab = document.getElementById("sentTab");

const receivedBox = document.getElementById("receivedBox");
const sentBox = document.getElementById("sentBox");

// Clique sur Reçus
receivedTab.addEventListener("click", () => {
    receivedTab.classList.add("active");
    sentTab.classList.remove("active");

    receivedBox.classList.remove("hidden");
    sentBox.classList.add("hidden");
});

// Clique sur Envoyés
sentTab.addEventListener("click", () => {
    sentTab.classList.add("active");
    receivedTab.classList.remove("active");

    sentBox.classList.remove("hidden");
    receivedBox.classList.add("hidden");
});

// pour naviguer entre les pages
let buttons = document.querySelectorAll("nav .same");

// gérer le clic (navigation)
buttons.forEach(btn => {
    btn.addEventListener("click", function() {
        let page = this.getAttribute("data-page");
        if (page) {
            window.location.href = page;
        }
    });
});

// gérer le bouton actif automatiquement
let currentPage = window.location.pathname.split("/").pop();

buttons.forEach(btn => {
    let page = btn.getAttribute("data-page");

    if (page === currentPage) {
        btn.classList.add("active");
    }
});