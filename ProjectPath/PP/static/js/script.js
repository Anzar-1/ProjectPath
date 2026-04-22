let projets = [
  { id: 1, titre: "GreenCity", description: "Projet écologique développé en lien avec l’environnement et les technologies vertes.", statut: "en attente" },
  { id: 2, titre: "Projet B", description: "Description du projet B", statut: "validé" },
  { id: 3, titre: "Projet C", description: "Description du projet C", statut: "refusé" }
];

let demandes = [
  { id: 1, type: "Financement", description: "Demande de budget pour GreenCity", statut: "en attente" },
  { id: 2, type: "Matériel", description: "Demande d’ordinateurs pour Projet B", statut: "initiée" },
  { id: 3, type: "Salle", description: "Réservation de salle pour Projet C", statut: "refusé" }
];

document.addEventListener("DOMContentLoaded", () => {
  navigate("dashboard");
});

function navigate(page) {
  const app = document.getElementById('app');
  if (page === 'dashboard') renderDashboard(app);
  if (page === 'project') renderProjectDetails(app, 1);
  if (page === 'messages') renderMessages(app);
}

function renderDashboard(app) {
  const total = projets.length;
  const enAttente = projets.filter(p => p.statut === "en attente").length;
  const valides = projets.filter(p => p.statut === "validé").length;
  const refuses = projets.filter(p => p.statut === "refusé").length;

  const totalDemandes = demandes.length;
  const enAttenteDem = demandes.filter(d => d.statut === "en attente").length;
  const approuveesDem = demandes.filter(d => d.statut === "approuvée").length;
  const refuseesDem = demandes.filter(d => d.statut === "refusée").length;
  const initieesDem = demandes.filter(d => d.statut === "initiée").length;

  app.innerHTML = `
  `;

  renderProjects();
  renderDemandes();
}

function renderProjects() {
  const list = document.getElementById("project-list");
  list.innerHTML = projets.map(p => `
  `).join("");
}

function updateStatus(id, newStatus) {
  const projet = projets.find(p => p.id === id);
  if (projet) projet.statut = newStatus;
  renderDashboard(document.getElementById('app'));
}

function renderDemandes(filter="tous", targetId="demandes-list") {
  const list = document.getElementById(targetId);
  let filtered = demandes;
  if (filter !== "tous") filtered = demandes.filter(d => d.statut === filter);

  list.innerHTML = filtered.map(d => `
   
  `).join("");
}

function updateDemandeStatus(id, newStatus, targetId="demandes-list") {
  const demande = demandes.find(d => d.id === id);
  if (demande) demande.statut = newStatus;
  renderDemandes("tous", targetId);
}

function renderProjectDetails(app, id) {
  const projet = projets.find(p => p.id === id);
  app.innerHTML = `
    <div class="tabs">
      <button class="active" onclick="showTab('vue', ${id})">Vue d’ensemble</button>
      <button onclick="showTab('besoins', ${id})">Demandes</button>
      <button onclick="showTab('documents', ${id})">Documents</button>
    </div>
    <div id="tab-content"></div>
  `;
  showTab("vue", id);
}

function showTab(tab, id) {
  const projet = projets.find(p => p.id === id);
  const content = document.getElementById("tab-content");

  if (tab === "vue") {
    content.innerHTML = `
      
    `;//Y avait le code de Project Details
  }

  if (tab === "besoins") {
    content.innerHTML = `
      <div class="filters">
        <button onclick="renderDemandes('tous','besoins-list')" class="active">Tous</button>
        <button onclick="renderDemandes('approuvée','besoins-list')">Acceptés</button>
        <button onclick="renderDemandes('refusée','besoins-list')">Refusés</button>
        <button onclick="renderDemandes('en attente','besoins-list')">En attente</button>
      </div>
      <div id="besoins-list"></div>
    `;
    renderDemandes("tous","besoins-list");
  }

  if (tab === "documents") {
    content.innerHTML = `<ul><li>Plan.pdf</li><li>Diagramme.png</li></ul>`;
  }
}

function updateStatusDetail(id, newStatus) {
  const projet = projets.find(p => p.id === id);
  if (projet) projet.statut = newStatus;
  // On recharge uniquement la vue détails, sans revenir au dashboard
  showTab("vue", id);
}

function saveComment(id) {
  const textarea = document.querySelector("textarea");
  if (textarea && textarea.value.trim() !== "") {
    localStorage.setItem("comment_" + id, textarea.value);
    alert("Commentaire enregistré !");
    textarea.value = "";
  }
}

function renderMessages(app) {
  app.innerHTML = `
    <h2>Messages</h2>
    <div class="messages-container">
      <div class="messages-list">Aucun message</div>
      <div class="message-content">Sélectionner un message pour le voir</div>
    </div>
  `;
}
