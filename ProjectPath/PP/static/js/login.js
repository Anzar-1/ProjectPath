const cnxBtns = document.querySelectorAll(".cnx");
const inscBtns = document.querySelectorAll(".insc");

const connexion = document.getElementById("connexion");
const inscription = document.getElementById("inscription");

// Connexion
cnxBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    connexion.classList.add("active");
    inscription.classList.remove("active");

    cnxBtns.forEach(b => b.classList.add("active"));
    inscBtns.forEach(b => b.classList.remove("active"));
  });
});

// Inscription
inscBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    inscription.classList.add("active");
    connexion.classList.remove("active");

    inscBtns.forEach(b => b.classList.add("active"));
    cnxBtns.forEach(b => b.classList.remove("active"));
  });
});