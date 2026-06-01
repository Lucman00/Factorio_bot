
# Factorio server discord Bot

A Discord bot for managing Factorio game servers via RCON with real-time status monitoring.

<img width="556" height="260" alt="Image" src="https://github.com/user-attachments/assets/046b4ea0-ee49-4937-9bdd-12185b37c1f3" />


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
```
- Python 3.10+
- rcon         ━┐
- python-dotenv ┤━pip install -r requirements.txt
- discord.py   ━┘
- Factorio server with RCON enabled
- Discord bot token 
```
## Installation

#### Method 1: Using Git Clone 
 ```bash
git clone https://github.com/Lucman00/Factorio_bot.git
cd factorio-discord-bot
```

#### Method 2: Using the zip

1.  [Download latest Release](https://github.com/Lucman00/Factorio_bot/releases/tag/stable)
2. Put the .zip file where you want your bot to be
3. extract the .zip file
___

once you have the archive extracted (or the cloned folder), it should look something like this
```
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
├──example.env.txt
├──main.py [this is the file you'll be running]
├──requirements.txt
└──README.md
```
next to the main.py, you'll create ```.env```, with the ```example.env.txt``` as a template for it (just copy paste it in)
once that's done you can fill out the fields inside of the ```.env```
    make sure that anything you fill in doesn't have a space in front |```DISCORD_TOKEN= [ETC]``` is wrong ```DISCORD_TOKEN=[ETC]``` is correct. no [""]. once thats done, you should be able to run the bot 


## Disclaimer
This was my first real project and first Discord bot. I learned as I built it, including working with RCON, asynchronous tasks, and role-based permissions. Feedback and contributions are welcome.
