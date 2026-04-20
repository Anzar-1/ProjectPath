const editBtn = document.getElementById("editBtn");
const saveBtn = document.getElementById("saveBtn");
const cancelBtn = document.getElementById("cancelBtn");

const inputs = document.querySelectorAll(".container input");

let oldValues = {};

// 👉 Modifier
editBtn.addEventListener("click", () => {
    inputs.forEach(input => {
        oldValues[input.id] = input.value;
        input.disabled = false;
    });

    editBtn.style.display = "none";
    saveBtn.style.display = "inline-block";
    cancelBtn.style.display = "inline-block";
});

// 👉 Sauvegarder
saveBtn.addEventListener("click", () => {
    inputs.forEach(input => {
        input.disabled = true;
    });

    editBtn.style.display = "inline-block";
    saveBtn.style.display = "none";
    cancelBtn.style.display = "none";
});

// 👉 Annuler
cancelBtn.addEventListener("click", () => {
    inputs.forEach(input => {
        input.value = oldValues[input.id];
        input.disabled = true;
    });

    editBtn.style.display = "inline-block";
    saveBtn.style.display = "none";
    cancelBtn.style.display = "none";
});

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