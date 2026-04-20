function addMember() {
  const container = document.getElementById("members");

  const newMember = document.createElement("div");
  newMember.classList.add("member");

  newMember.innerHTML = `
    <h3></h3>
    <input type="text" placeholder="Nom complet">
    <input type="text" placeholder="Rôle">
    <input type="email" placeholder="Email">
  `;

  container.appendChild(newMember);
  updateMembers();
}

function removeMember(btn) {
  btn.parentElement.remove(); // supprime toute la case
  updateMembers();
}

function updateMembers() {
  const members = document.querySelectorAll(".member");

  members.forEach((member, index) => {
    // Mise à jour du numéro
    member.querySelector("h3").innerText = "Membre " + (index + 1);

    // Supprimer ancien bouton s'il existe
    let oldBtn = member.querySelector(".remove-btn");
    if (oldBtn) oldBtn.remove();

    // 👉 Ajouter bouton SEULEMENT si +1 membre
    if (members.length > 1) {
      const btn = document.createElement("button");
      btn.className = "remove-btn";
      btn.innerText = "-";
      btn.onclick = function() { removeMember(btn); };
      member.appendChild(btn);
    }
  });
}

// Initialisation
updateMembers();

// gérer le bouton actif automatiquement
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