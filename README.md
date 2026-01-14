# Steam Completionist Optimizer (Local Dashboard)

A real-time, local web dashboard that tracks your Steam achievement progress. It analyzes global player statistics to suggest the **"Optimal Route"** (easiest achievements first) and provides visual "Toast" notifications when you unlock an achievement in-game.

Built with **Python (Flask)**, **HTML/CSS**, and **JavaScript**.

## ✨ Features

* **Real-Time Tracking:** Polls the Steam API to detect changes while you play.
* **Optimal Route Algorithm:** Sorts incomplete achievements by "Global Rarity," suggesting the most common (easiest) achievements to target next.
* **Live Notifications:** A gold popup toast appears on the dashboard the moment an achievement is unlocked.
* **Game Switcher:** Input any Steam App ID to instantly load data for a different game.
* **Steam-Themed UI:** Dark mode interface inspired by the Steam client.

## 🛠️ Prerequisites

Before running the app, you need the following:

1.  **Python 3.x** installed.
2.  **Steam Web API Key:** [Get it here](https://steamcommunity.com/dev/apikey).
3.  **Your Steam ID (64-bit):** [Find it here](https://steamid.io/).
4.  **Public Profile:** Your Steam Privacy settings for "Game Details" must be set to **Public**.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/steam-achievement-tracker.git](https://github.com/yourusername/steam-achievement-tracker.git)
    cd steam-achievement-tracker
    ```

2.  **Install dependencies:**
    ```bash
    pip install flask requests
    ```

## ⚙️ Configuration

1.  Open `app.py`.
2.  Locate the configuration section at the top:
    ```python
    # --- CONFIGURATION ---
    STEAM_API_KEY = 'YOUR_STEAM_API_KEY_HERE'
    STEAM_USER_ID = 'YOUR_STEAM_64_ID_HERE'
    ```
3.  Replace the placeholders with your actual API Key and Steam User ID.

## 🚀 How to Run

1.  **Start the server:**
    ```bash
    python app.py
    ```
2.  **Open the dashboard:**
    Go to `http://127.0.0.1:5000` in your web browser.
3.  **Enter a Game ID:**
    * Find the App ID in the Steam Store URL (e.g., for *Elden Ring*, the URL is `store.steampowered.com/app/1245620`, so the ID is `1245620`).
    * Enter `1245620` into the dashboard and click **Load Game**.

## 📂 Project Structure

```text
steam_tracker/
│
├── app.py                # Flask Backend (API & Logic)
├── templates/
│   └── index.html        # Frontend HTML
└── static/
    ├── style.css         # Styling (Steam Dark Theme)
    └── script.js         # Frontend Logic (Polling & UI Updates)
