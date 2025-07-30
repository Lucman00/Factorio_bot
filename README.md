
# Factorio server discord Bot

A Discord bot for managing Factorio game servers via RCON with real-time status monitoring.

![Control Panel Example](https://imgur.com/gallery/control-panel-example-77Cf6hF)
## Features

- **Server Control**:
    - Start/Stop server with buttons
    - Manual save triggering
    - Status updates every 25 seconds (Adjustable)
- **User Management**:
  - A Role-based permission system (Default: only "Factorio" roles can interact with the server panel
  - Shows player list
  - Admin-only commands

- **Technical**:
  - logs connections to rcon and any errors inside the "logs" folder

## Prerequisites
- Python 3.10+
- Factorio server with RCON enabled
- Discord bot token
## Installation

First of all, your server.bat should look something like this

```bash
start /wait bin\x64\factorio.exe --start-server saves\[save file.zip] ^
--server-settings "server-settings.json" ^
--port [your chosen factorio port] ^
--rcon-port [your chosen rcon-port] ^
--rcon-password [your chosen rcon-password] ^
--no-log-rotation
pause
```
Important here is the rcon-port and passwordas that allows the bot to communicate with the server. 

Then you can download the bot itself
#### Method 1: Using Git Clone (*Recommended*)
 ```bash
git clone https://github.com/Lucman00/Factorio_bot.git
cd factorio-discord-bot```

#### Method 2: Using the zip

1.  [Download the zip](github.com/lucman00/factorio_bot/archive/refs/heads/main.zip)
2. Put the .zip file where you want your bot to be
3. extract the .zip file


once you have the archive extracted, it should look something like this

Factorio_bot
│
├──factorio_bot
│   ├──R_con
│   ├──server
│   ├──tasks
│   ├──ui
│   ├──utils
│   │
│   ├──__init_.py
│   ├──bot.py
│   ├──config.py
│   ├──constants.py
│   └──exceptions.py
├──.env    [this is the file you'll have to put your discord token and directory into]
├──main.py [this is the file you'll be running]
└──README.md

In the last step you will have to open the .env and put in your
discord token, discord channel id, rcon ip ("rcon_host"),
rcon_password, the rcon port(both of these HAVE to be the same as in
the bat file) and lastly your server_path. 
