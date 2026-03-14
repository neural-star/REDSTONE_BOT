import os
import discord
from discord import app_commands

SQL_PATHs = {"main": "sql\\main.db", "hub": "sql\\hub.db", "wiki": "sql\\wiki.db"}
HUB_CHANNEL_ID: str = os.getenv("HUB_CHANNEL_ID")
LOG_CHANNEL_ID: str = os.getenv("LOG_CHANNEL_ID")
TOKEN: str = os.getenv("TOKEN")
MAIN_SERVER_ID: str = os.getenv("MAIN_SERVER_ID")
WIKI_CHANNEL_ID: str = os.getenv("WIKI_CHANNEL_ID")
WIKI_ROLE_ID: str = os.getenv("WIKI_ROLE_ID")

if all([HUB_CHANNEL_ID, LOG_CHANNEL_ID, TOKEN, MAIN_SERVER_ID, WIKI_CHANNEL_ID]):
    MAIN_SERVER_ID = int(MAIN_SERVER_ID)
    WIKI_CHANNEL_ID = int(WIKI_CHANNEL_ID)
    WIKI_ROLE_ID = int(WIKI_ROLE_ID)
else:
    raise ValueError("必要な環境変数が設定されていません")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
