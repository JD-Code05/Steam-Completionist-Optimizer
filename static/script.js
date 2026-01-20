let currentAppId = '12210'; 
let currentSteamId = '76561198979373921'; 
let knownAchievements = new Set();
let firstRun = true;
let refreshInterval; 

function updateProfile() {
    const inputVal = document.getElementById('steamIdInput').value;
    
    if (inputVal.length > 10) {
        currentSteamId = inputVal;
        const btn = document.querySelector('button[onclick="updateProfile()"]');
        const originalText = btn.innerText;
        btn.innerText = "Saved! ✓";
        setTimeout(() => btn.innerText = originalText, 2000);
        
        const titleElement = document.getElementById('gameTitle');
        const currentText = titleElement.innerText;
        const gameName = currentText.replace('Currently Tracking: ', '').trim();
        
        loadGameData(currentAppId, gameName);
    } else {
        alert("Please enter a valid Steam ID64 (starts with 765...)");
    }
}

async function searchGames() {
    const query = document.getElementById('searchInput').value;
    const resultsDiv = document.getElementById('searchResults');
    
    if (query.length < 3) return;

    resultsDiv.style.display = 'block';
    resultsDiv.innerHTML = '<div class="result-item">Searching...</div>';

    try {
        const response = await fetch(`/api/search?q=${query}`);
        const games = await response.json();

        resultsDiv.innerHTML = ''; 

        if (games.length === 0) {
            resultsDiv.innerHTML = '<div class="result-item">No games found</div>';
            return;
        }

        games.forEach(game => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerText = game.name;

            div.onmousedown = function() {
                console.log("Game Selected:", game.name); 
                currentAppId = game.id;
                firstRun = true; 
                knownAchievements.clear();
                
                loadGameData(game.id, game.name);
                
                resultsDiv.style.display = 'none';
                resultsDiv.innerHTML = ''; 
                document.getElementById('searchInput').value = ''; 
            };
            
            resultsDiv.appendChild(div);
        });

    } catch (error) {
        console.error("Search Error:", error);
        resultsDiv.innerHTML = '<div class="result-item" style="color:red;">Error searching</div>';
    }
}

async function loadGameData(appId, gameName) {
    if (gameName) {
        document.getElementById('gameTitle').innerHTML = `Currently Tracking: <span style="color: #00d2ff;">${gameName}</span>`;
    }

    try {
        const response = await fetch(`/api/data?app_id=${appId}&steam_id=${currentSteamId}`);
        const data = await response.json();

        const list = document.getElementById('achievementsList');
        list.innerHTML = ''; 

        if (data.length === 0) {
            list.innerHTML = '<p>No achievements found. (Profile might be private, or game not owned).</p>';
            return;
        }

        let completedCount = 0;

        data.forEach((ach, index) => {
            const card = document.createElement('div');
            card.className = `achievement-card ${ach.achieved ? 'achieved' : ''}`;

            if (!ach.achieved && index < (completedCount + 3)) {
                card.classList.add('recommended');
                card.innerHTML += `<div style="color:#ffd700; font-weight:bold; font-size:0.8em; margin-bottom:5px; text-shadow:0 0 5px rgba(255, 215, 0, 0.5);">RECOMMENDED NEXT</div>`;
            }

            const statusIcon = ach.achieved ? '✅' : '🔒';
            const rarityVal = ach.rarity ? ach.rarity.toFixed(1) : "0.0";

            card.innerHTML += `
                <strong>${statusIcon} ${ach.name}</strong>
                <span style="float:right; color: #a68eff; font-size:0.9em;">${rarityVal}% Global</span>
                <br>
                <small style="color: #bbb;">${ach.description}</small>
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

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function showToast(title, desc) {
    const toast = document.getElementById('toast');
    document.getElementById('toast-title').innerText = "🏆 UNLOCKED: " + title;
    document.getElementById('toast-desc').innerText = desc;
    toast.classList.remove('hidden'); 
    setTimeout(() => { toast.classList.add('hidden'); }, 5000);
}

document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') searchGames();
});

loadGameData(currentAppId, 'Grand Theft Auto IV: The Complete Edition');

clearInterval(refreshInterval);
refreshInterval = setInterval(() => { loadGameData(currentAppId); }, 10000);