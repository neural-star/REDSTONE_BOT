import threading

import discord

from config import client,tree,TOKEN
from cogs import *
from initialize import init
from keep_alive import app
from UI.buttons import Wiki_View

@client.event
async def on_ready():
    await tree.sync()
    client.add_view(Wiki_View())
    print(f'We have logged in as {client.user}')

@tree.command(name="ping", description="Ping Pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong!{interaction.client.latency * 1000:.2f}ms", ephemeral=True)

def run_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    init()
    threading.Thread(target=run_flask).start()
    if TOKEN:
        client.run(TOKEN)
    else:
        print("Error: TOKEN is not str")
