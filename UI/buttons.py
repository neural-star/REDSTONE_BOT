import discord

from config import WIKI_ROLE_ID
from utils.role import has_wiki_role

class Wiki_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="編集", style=discord.ButtonStyle.primary, custom_id="wiki_edit")
    async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_wiki_role(interaction, WIKI_ROLE_ID):
            await interaction.response.send_message("この操作にはWIKIロールが必要です。", ephemeral=True,)
            return
        message = interaction.message
        name = message.content.split("="*10)[1]
        from cogs.wiki import add_wiki
        await add_wiki(interaction, name, message)
