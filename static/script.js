let knownAchievements = new Set();
let firstRun = true;

async function updateData(){
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
        }
    }
}