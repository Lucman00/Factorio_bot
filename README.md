# Factorio Server Discord Bot

A Discord bot for managing Factorio game servers via RCON with real-time status monitoring.

<img width="556" height="260" alt="Image" src="https://github.com/user-attachments/assets/046b4ea0-ee49-4937-9bdd-12185b37c1f3" />

## Features

- **Server Control** — Start/stop the server with buttons, manual save triggering, status updates every 25 seconds (adjustable)
- **User Management** — Role-based permission system (default: only users with the "Factorio" role can interact with the panel), player list, admin-only commands
- **Technical** — Logs RCON connections and errors to the `logs/` folder

## Prerequisites

- Python 3.8+
- A Factorio server with RCON enabled
- A Discord bot token

## Installation

### Method 1: Automatic (recommended)

**Linux:**
```bash
bash install.sh
```
Or with curl (no manual download needed):
```bash
curl -fsSL https://github.com/Lucman00/Factorio_bot/releases/latest/download/install.sh | bash
```

**Windows:**

Download and run `install.bat` from the [latest release](https://github.com/Lucman00/Factorio_bot/releases/latest).

The install script will:
- Check for Python 3.8+ and install it if missing
- Clone this repository
- Create a virtual environment
- Install all dependencies
- Prompt you for your Discord token, channel ID, and Factorio server path and write your `.env`

### Method 2: Manual

```bash
git clone https://github.com/Lucman00/Factorio_bot.git
cd Factorio_bot
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Then fill in `.env` with your values (see Configuration below).

## Configuration

All configuration lives in `.env`. Copy `.env.example` as a starting point:

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `DISCORD_TOKEN` | ✅ | — | Your Discord bot token |
| `DISCORD_CHANNEL_ID` | ✅ | — | Channel ID for the control panel |
| `RCON_PASSWORD` | ✅ | — | Your Factorio server RCON password |
| `SERVER_PATH` | ✅ | — | Absolute path to your Factorio server folder |
| `RCON_HOST` | | `127.0.0.1` | RCON host (change if bot runs on a different machine) |
| `RCON_PORT` | | `27015` | RCON port |
| `GAME_PORT` | | `34197` | Factorio game port |
| `SAVE_GAMES_DIR` | | `saves` | Save directory, relative to `SERVER_PATH` |
| `STATUS_UPDATE_INTERVAL` | | `25` | How often (seconds) the panel refreshes |

> Make sure there are no spaces around `=` in your `.env`. `TOKEN=abc` is correct, `TOKEN= abc` is not.

## Running the bot

**Linux:**
```bash
bash run.sh
```

**Windows:**
```bat
run.bat
```

### Running as a persistent service (Linux, recommended for servers)

To have the bot start automatically on boot and restart on crash, set it up as a systemd service:

1. Create the service file:
```bash
sudo nano /etc/systemd/system/factorio-bot.service
```

2. Paste this, replacing the path with wherever you cloned the repo:
```ini
[Unit]
Description=Factorio Discord Bot
After=network.target

[Service]
WorkingDirectory=/path/to/Factorio_bot
ExecStart=/path/to/Factorio_bot/venv/bin/python main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Enable and start it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable factorio-bot
sudo systemctl start factorio-bot
```

Check logs with `journalctl -u factorio-bot -f`.

## Project structure

```
Factorio_bot/
│
├── factorio_bot/
│   ├── R_con/          # RCON client and commands
│   ├── server/         # Server monitor and controller
│   ├── tasks/          # Background status updater
│   ├── ui/             # Discord embeds and views
│   ├── utils/          # Logging, decorators, persistence
│   ├── bot.py
│   ├── config.py
│   ├── constants.py
│   └── exceptions.py
├── .env.example
├── main.py
└── requirements.txt
```

## Disclaimer

This was my first real project and first Discord bot. I learned as I built it, including working with RCON, asynchronous tasks, and role-based permissions. Feedback and contributions are welcome.