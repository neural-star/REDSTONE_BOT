import discord

class FlexibleButtons(discord.ui.View):
    def __init__(self, allowed_user_id: int, buttons_info: list, disabled: bool = True, data = None):
        """
        buttons_info: [(label:str, func:async function, style:discord.ButtonStyle), ...]
        """
        super().__init__(timeout=None)
        self.allowed = allowed_user_id
        self.disabled = disabled
        self.data = data

        for i, (label, func, style) in enumerate(buttons_info):
            btn = discord.ui.Button(label=label, style=style, custom_id=f"flex_button_{i}")
            btn.callback = self._make_callback(func)
            self.add_item(btn)

    def _make_callback(self, func):
        async def callback(interaction: discord.Interaction):
            if self.allowed and interaction.user.id != self.allowed:
                await interaction.response.send_message("❌あなたはこのボタンを使用できません！", ephemeral=True)
                return 
            
            if self.disabled:
                for item in self.children:
                    if isinstance(item, discord.ui.Button) and item.custom_id and item.custom_id.startswith("flex_button_"):
                        item.disabled = True
                await interaction.response.edit_message(view=self)
            
            await func(interaction, self.data, self)
        return callback
