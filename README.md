<div align="center">

# Steam Completionist Optimizer
### A Local Achievement Tracking Dashboard

![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<br>

<img src="dashboard-preview.png" alt="Steam Completionist Dashboard" width="800" style="border-radius: 10px; box-shadow: 0px 0px 20px rgba(0,0,0,0.5);">

<br><br>

A real-time, local web dashboard that tracks your Steam achievement progress. It analyzes global player statistics to suggest the **"Optimal Route"** (easiest achievements first) and provides visual "Toast" notifications when you unlock an achievement in-game.

</div>

---

## Key Features

| Feature | Description |
| :--- | :--- |
| **Real-Time Polling** | Automatically polls the Steam API every 10 seconds to detect in-game unlocks without refreshing the page. |
| **Optimization Algorithm** | Sorts incomplete achievements by "Global Rarity," intelligently suggesting the most common (easiest) achievements to target next. |
| **Schema Translation** | Maps raw developer API codes (e.g., `E1INTRO`) to human-readable titles and descriptions using the Game Schema. |
| **Game Switcher** | Built-in search bar allows you to find and switch games instantly without needing to look up manual App IDs. |

---

## Repository Structure

```text
steam-completionist-optimizer/
│
├── Completionist.py      # Flask Backend (API, Data Fetching & Logic)
├── templates/
│   └── index.html        # Frontend HTML Structure
└── static/
    ├── style.css         # Styling (Steam Dark Theme & Animations)
    └── script.js         # Frontend Logic (Polling, Search, & UI Updates)
```

---

## Quick Start  
### 1. Clone the Repository  
```text
git clone [https://github.com/yourusername/steam-completionist-optimizer.git](https://github.com/yourusername/steam-completionist-optimizer.git)
cd steam-completionist-optimizer
```

### 2. Install Dependencies  
```text
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
# Install required packages
pip install flask requests
```

### 3. Configuration  
Open Completionist.py in your text editor and update the constants at the top:  
```text
# Completionist.py

STEAM_API_KEY = 'YOUR_ACTUAL_STEAM_API_KEY'
DEFAULT_STEAM_ID = 'YOUR_ACTUAL_STEAM_ID'
```

### 4. Run the Application  
```text
python Completionist.py
```
    The dashboard will start at http://127.0.0.1:5000
