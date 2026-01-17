let knownAchievements = new Set();
let firstRun = true;

async function updateData() {
    try {
        const response = await fetch('/api.data');
        const data = await response.json();

        const list = document.getElementById('achievement-list');
        list.innerHTML = '';

        let completedCount = 0;

        data.forEach((ach, index) => {
            const card = document.createElement('div');
            card.className = `card ${ach.achieved ? 'completed' : ''}`;

            if (!ach.achieved && index < 3 + completedCount) {
                card.classList.add('recommended');
                card.innerHTML += `<div style="color:#a4d007; font-weight:bold; font-size:0.8em">RECOMMENDED NEXT</div>`;
            }
            card.innerHTML += `
                <h3>${ach.name}</h3>
                <p>${ach.description}</p>
                <small>${ach.rarity.toFixed(1)}% Global Unlock</small>
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
