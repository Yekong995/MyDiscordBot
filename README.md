# MyDiscordBot

## Description

This Discord bot is a project made by me during self learning Python.

**If you need using music function please download `ffmpeg` and add it to path before using music command otherwise it will no effect**



## Table Content

> [Requirements](#requirements)
>
> [How To Use](#how-to-use)
>
> [Setup Token](#token)
>
> [Setup Prefix](#setup-prefix)
>
> [Get Command](#get-command)



## Requirements

> - [Python 3.8+](https://www.python.org/downloads/)
> - [PIP](https://pip.pypa.io/en/stable/installation/)
> - [FFMPEG](https://ffmpeg.org/download.html)

**Linux (Using dnf)**

```bash
sudo dnf install ffmpeg-free -y
```

**Linux (Using apt)**

```bash
sudo apt install ffmpeg -y
```



## How To Use

OS      |Python Version
--------|---------------
Windows |Python3.8+
Linux   |Python3

### Windows

```bash
pip install -r requirements.txt -U
python main.py
```

### Linux (Using apt)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
pip install -r requirements.txt -U
python3 main.py
```

### Linux (Using dnf)

```bash
sudo dnf updateinfo && sudo dnf upgrade -y
sudo dnf install python3 python3-pip -y
pip install -r requirements.txt -U
python3 main.py
```



### Virtual Environment

```bash
pip install -U pipenv
pipenv sync
pipenv shell # This will let you enter virtual environment, enter exit to exit virtual environment
python main.py
```



## Token

1. Go to [Dsicord Developer Portal](https://github.com/Yekong995/MyDiscordBot.git)
2. Click at the `New Application` button to create a new application
![New_Application_Button](image/capp.png)
3. Click at the `Bot` option
4. Open all intents option
![Option_Intents](image/intents.png)
5. Press the `Reset Token` to show the token of your bot and copy it
6. Go to `OAuth2` option and go to `URL Generator`
7. In the scopes select `bot`
8. Go down select `Administrator` (Recommended) else see [Permission](#Permission) to choices
9. Create a new file name `.env` or change filename `.env.template` to `.env`
10. Open `.env` with any editor you love and input `DISCORD_TOKEN=<your token here>`
11. Save & Close the file after edited [How To Use](#How-To-Use)



## Permission

The following are the necessary permissions:

Permission                 |
---------------------------|
Manage Role                |
Manage Channels            |
Kick Members               |
Ban Members                |
Read Messages/View Channels|
Send Messages              |
Manage Messages            |
Embed Links                |
Attach Files               |
Read Message History       |
Connect                    |
Speak                      |



## Setup Prefix

Change `command_prefix="<your_prefix_here>"` in file `main.py` line 26

    26| client = Bot(command_prefix=">", intents=intents, description="My Command List")



## Get Command

Type `>help` to show all the commands. (Commands will be displayed based on permissions)

> NOTE: If you change your prefix please change `>` to the prefix you set
