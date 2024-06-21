# Description

This Discord bot is a project made by me during self learning Python.

**If you need using music function please download `ffmpeg` and add it to path before using music command otherwise it will no effect**



[TOC]



# Requirements

> - [Python 3.8+](https://www.python.org/downloads/)
> - [Pip](https://pip.pypa.io/en/stable/installation/)
> - [FFmpeg](https://ffmpeg.org/download.html)



# Install dependencies

## Local

```bash
pip install -r requirements.txt -U
python main.py
```

## Virtual Environment

```bash
pip install -U pipenv
pipenv update
pipenv shell # Enter virtual environment, type exit to escape virtual environment
python main.py
```



# Token

Get it from [Discord Developer Portal](https://discord.com/developers/applications)



# Permission

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



# Setup Prefix

Change `prefix="<your_prefix_here>"` in file `main.py` line 28

    28| prefix = ">"



# Command List

Type `>help` to show all the commands. (Commands will be displayed based on permissions)

> NOTE: If you change your prefix please change `>` to the prefix you set