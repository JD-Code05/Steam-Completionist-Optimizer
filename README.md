# Steam Completionist Optimizer (Local Dashboard)  
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) 
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)    

A real-time, local web dashboard that tracks your Steam achievement progress. It analyzes global player statistics to suggest the **"Optimal Route"** (easiest achievements first) and provides visual "Toast" notifications when you unlock an achievement in-game.

Built with **Python (Flask)**, **HTML/CSS**, and **JavaScript**.

---

## Features

* **Real-Time Tracking:** Polls the Steam API every 10 seconds to detect changes while you play.
* **Optimal Route Algorithm:** Sorts incomplete achievements by "Global Rarity," automatically suggesting the most common (easiest) achievements to target next.
* **Live Notifications:** A gold popup toast appears on the dashboard the moment an achievement is unlocked.
* **Game Switcher:** Built-in search bar allows you to find and switch games instantly without needing App IDs.
* **Steam-Themed UI:** Dark mode interface inspired by the Steam client.

---

## Prerequisites

Before running the app, you need the following:

1.  **Python 3.x** installed.
2.  **Steam Web API Key:** [Get it here](https://steamcommunity.com/dev/apikey).
3.  **Your Steam ID (64-bit):** [Find it here](https://steamid.io/).
4.  **Public Profile:** Your Steam Privacy settings for "Game Details" must be set to **Public**.

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/steam-completionist-optimizer.git](https://github.com/yourusername/steam-completionist-optimizer.git)
    cd steam-completionist-optimizer
    ```

2.  **Install dependencies:**
    ```bash
    pip install flask requests
    ```

---

## ⚙️ Configuration

1.  Open `Completionist.py`.
2.  Locate the configuration section at the top:
    ```python
    STEAM_API_KEY = 'YOUR_STEAM_API_KEY_HERE'
    DEFAULT_STEAM_ID = 'YOUR_STEAM_ID_HERE'
    ```
3.  Replace the placeholders with your actual API Key and Steam User ID.

> **Optional:** You can also update `static/script.js` line 2 (`let currentSteamId = ...`) if you want the frontend to load your ID by default without needing to enter it in the UI every time.

---

## 🚀 How to Run

1.  **Start the server:**
    ```bash
    python Completionist.py
    ```
2.  **Open the dashboard:**
    Go to `http://127.0.0.1:5000` in your web browser.
3.  **Use the Dashboard:**
    * **Set ID:** If you didn't hardcode your ID in the script, enter your Steam ID64 in the top input box and click "Set ID".
    * **Search Game:** Type a game name (e.g., "Hades") in the search bar.
    * **Track:** Click the game from the dropdown results to instantly load your achievement progress.

---

## Project Structure

```text
steam-completionist-optimizer/
│
├── Completionist.py      # Flask Backend (API, Data Fetching & Logic)
├── templates/
│   └── index.html        # Frontend HTML Structure
└── static/
    ├── style.css         # Styling (Steam Dark Theme & Animations)
    └── script.js         # Frontend Logic (Polling, Search, & UI Updates)