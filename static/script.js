let currentAppId = '12210';
let currentSteamId = 'YOUR_STEAM_ID_HERE';
let knownAchievements = new Set();
let firstRun = true;
let refreshInterval;

function updateProfile() {
    const inputVal = document.getElementById('steamIdInput').value;
    if (inputVal.length > 10) {
        currentSteamId = inputVal;
        loadGameData(currentAppId);
    } else {
        alert("Invalid Steam ID");
    }
}

async function searchGames() {
    const query = document.getElementById('searchInput').value;
    const resultsDiv = document.getElementById('searchResults');
    if (query.length < 3) return;

    resultsDiv.innerHTML = 'Searching...';

    const response = await fetch(`/api/search?q=${query}`);
    const games = await response.json();
    resultsDiv.innerHTML = '';

    games.forEach(game => {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerText = game.name;
        div.onclick = () => {
            currentAppId = game.id;
            knownAchievements.clear();
            firstRun = true;
            loadGameData(game.id, game.name);
            resultsDiv.innerHTML = '';
        };
        resultsDiv.appendChild(div);
    });
}

async function loadGameData(appId, gameName) {
    if (gameName) {
        document.getElementById('gameTitle').innerHTML =
            `Currently Tracking: <span style="color:#00d2ff;">${gameName}</span>`;
    }

    const response = await fetch(`/api/data?app_id=${appId}&steam_id=${currentSteamId}`);
    const data = await response.json();

    const list = document.getElementById('achievementsList');
    list.innerHTML = '';

    let completedCount = 0;

    data.forEach((ach, index) => {
        const card = document.createElement('div');
        card.className = `achievement-card ${ach.achieved ? 'achieved' : ''}`;

        if (!ach.achieved && index < 3) {
            card.classList.add('recommended');
            card.innerHTML += `<div style="color:#ffd700;">RECOMMENDED NEXT</div>`;
        }

        card.innerHTML += `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 5px;">
                
                <div style="display: flex; align-items: flex-start; gap: 6px; flex: 1;">
                    <span style="flex-shrink: 0;">${ach.achieved ? '✅' : '🔒'}</span>
                    <strong style="word-break: break-word; line-height: 1.2;">${ach.name}</strong>
                </div>
                
                <span style="white-space: nowrap;">${ach.rarity.toFixed(1)}%</span>
            </div>
            <small style="display: block; color: #aaaaaa; line-height: 1.4;">${ach.description}</small>
        `;

        list.appendChild(card);

        if (ach.achieved) completedCount++;

        if (!firstRun && ach.achieved && !knownAchievements.has(ach.apiname)) {
            showToast(ach.name, ach.description);
        }

        if (ach.achieved) knownAchievements.add(ach.apiname);
    });

    const percent = ((completedCount / data.length) * 100).toFixed(1);
    const bar = document.getElementById('progressBar');
    bar.style.width = percent + '%';
    bar.innerText = percent + '%';

    firstRun = false;
}

function showToast(title, desc) {
    const toast = document.getElementById('toast');
    document.getElementById('toast-title').innerText = "🏆 UNLOCKED: " + title;
    document.getElementById('toast-desc').innerText = desc;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 5000);
}

loadGameData(currentAppId);
clearInterval(refreshInterval);
refreshInterval = setInterval(() => loadGameData(currentAppId), 10000);