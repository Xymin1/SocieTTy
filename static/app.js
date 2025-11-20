const phaseInput = document.getElementById("phase-id");
const phaseTitle = document.getElementById("phase-title");
const matchesGrid = document.getElementById("matches");
const teamsTable = document.getElementById("teams");
const playersTable = document.getElementById("players");
const statusText = document.getElementById("status");
const toast = document.getElementById("toast");

const formatter = new Intl.DateTimeFormat("pl-PL", {
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
});

function showToast(message, isError = false) {
  toast.textContent = message;
  toast.style.borderColor = isError ? "var(--danger)" : "rgba(255,255,255,0.1)";
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

function renderMatches(matches) {
  matchesGrid.innerHTML = "";
  if (!matches.length) {
    matchesGrid.innerHTML = '<p class="meta">Brak danych o meczach.</p>';
    return;
  }

  matches.forEach((match) => {
    const card = document.createElement("article");
    card.className = "card";

    const date = match.match_date ? formatter.format(new Date(match.match_date)) : "TBA";
    const score = match.score ?? "-";

    card.innerHTML = `
      <div class="card-header">
        <h3>${match.home_team} <span class="meta">vs</span> ${match.away_team}</h3>
        <span class="stat">${score}</span>
      </div>
      <div class="status">
        <span class="badge">${match.round || "Harmonogram"}</span>
        <span>${date}</span>
      </div>
    `;

    matchesGrid.appendChild(card);
  });
}

function renderTeams(teams) {
  teamsTable.innerHTML = "";
  if (!teams.length) {
    teamsTable.innerHTML = '<tr><td colspan="6" class="meta">Brak tabeli.</td></tr>';
    return;
  }

  const rows = teams
    .map(
      (team) => `
      <tr>
        <td>${team.position}</td>
        <td>${team.name}</td>
        <td>${team.matches_played ?? "-"}</td>
        <td>${team.points ?? "-"}</td>
        <td>${team.sets_balance ?? "-"}</td>
        <td>${team.games_balance ?? "-"}</td>
      </tr>
    `
    )
    .join("");

  teamsTable.innerHTML = rows;
}

function renderPlayers(players) {
  playersTable.innerHTML = "";
  if (!players.length) {
    playersTable.innerHTML = '<tr><td colspan="5" class="meta">Brak rankingu.</td></tr>';
    return;
  }

  const rows = players
    .map(
      (player) => `
      <tr>
        <td>${player.position}</td>
        <td>${player.name}</td>
        <td>${player.club ?? "-"}</td>
        <td>${player.balance ?? "-"}</td>
        <td>${player.points ?? "-"}</td>
      </tr>
    `
    )
    .join("");

  playersTable.innerHTML = rows;
}

async function fetchPhase() {
  const phaseId = Number(phaseInput.value);
  if (!phaseId) {
    showToast("Wpisz ID fazy z liga.kozts.pl", true);
    return;
  }

  statusText.textContent = "Ładowanie danych...";
  try {
    const response = await fetch(`/api/phase/${phaseId}`);
    if (!response.ok) {
      throw new Error(`API zwróciło ${response.status}`);
    }

    const payload = await response.json();
    phaseTitle.textContent = payload.title || `Faza ${phaseId}`;
    renderMatches(payload.matches || []);
    renderTeams(payload.teams || []);
    renderPlayers(payload.players || []);
    statusText.textContent = `Ostatnia aktualizacja: ${formatter.format(new Date(payload.updated_at))}`;
    showToast("Dane załadowane!", false);
  } catch (error) {
    console.error(error);
    statusText.textContent = "Nie udało się pobrać danych. Spróbuj ponownie.";
    showToast(error.message, true);
  }
}

phaseInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    fetchPhase();
  }
});

document.getElementById("load-phase").addEventListener("click", fetchPhase);

fetchPhase();
