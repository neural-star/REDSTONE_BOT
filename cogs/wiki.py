import discord

import asyncio

from config import client, tree, MAIN_SERVER_ID, WIKI_CHANNEL_ID, SQL_PATHs, WIKI_ROLE_ID
from UI.buttons import Wiki_View
from utils import thread_crt
from utils.sql_crt import SQLCtr
from utils.role import has_wiki_role

async def add_wiki(interaction:discord.Interaction, name:str, MESSAGE:discord.Message | None = None):
    await interaction.response.send_message("追加するページの内容を送信してください", ephemeral=True)
    
    guild = client.get_guild(MAIN_SERVER_ID)
    channel = guild.get_channel(WIKI_CHANNEL_ID)
        
    def check(message: discord.Message):
            return (
                message.author == interaction.user
                and message.channel == interaction.channel
            )
        
    try:
        user_message = await client.wait_for("message", check=check, timeout=300)
        content = user_message.content

        try:
            await user_message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass
        
        header = "=" * 10
        message = f"{header}{name}{header}\n{content}"
        view = Wiki_View()
        
        if MESSAGE:
            await MESSAGE.edit(content=message)
            await interaction.followup.send("投稿の編集が完成しました", ephemeral=True)
        else:
            await channel.send(message, view=view)
            await interaction.followup.send("投稿が完了しました", ephemeral=True)
        
        thread = await thread_crt.create_thread(
            interaction=interaction,
            channel_id=WIKI_CHANNEL_ID,
            name=name,
            server_id=MAIN_SERVER_ID,
            lock=True)
        
        await thread.send(f"{interaction.user.display_name}({interaction.user.id})\n{message}")
        
        if not MESSAGE:
            SQL = SQLCtr(SQL_PATHs["wiki"])
            data = {"name": name, "thread_id": thread.id}
            SQL.insert("Pages", data)

    except asyncio.TimeoutError:
        await interaction.followup.send("時間切れです。もう一度/create_pageを使用してください", ephemeral=True)

def main():
    @tree.command(name="create_page", description="Wikiに新たにページを追加します")
    async def create_page(interaction: discord.Interaction, name:str):
        if not has_wiki_role(interaction, WIKI_ROLE_ID):
            await interaction.response.send_message("この操作にはWIKIロールが必要です。", ephemeral=True,)
            return
        await add_wiki(interaction,name)
    
    @tree.command(name="get_wiki", description="Wiki内の投稿から指定したページを取得します")
    async def get_page(interaction: discord.Interaction, name:str):
        SQL = SQLCtr(SQL_PATHs["wiki"])
        data = SQL.select("Pages")
        thread_id = None
        
        for dict in data:
            if dict["name"] == name:
                thread_id = dict["thread_id"]
                break

        if thread_id is None:
            await interaction.response.send_message("指定されたページが存在しませんでした")
        else:
            guild = client.get_guild(MAIN_SERVER_ID)
            channel = guild.get_channel(WIKI_CHANNEL_ID)
            thread = channel.get_thread(thread_id)
            
            message = await thread.fetch_message(thread.last_message_id)
            
            await interaction.response.send_message(message.content, ephemeral=True)
        