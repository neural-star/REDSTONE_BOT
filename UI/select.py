import discord

class MySelect(discord.ui.Select):
    def __init__(self,option:dict):
        options = [
            discord.SelectOption(label="りんご", value="apple"),
            discord.SelectOption(label="みかん", value="orange"),
            discord.SelectOption(label="バナナ", value="banana")
        ]

        super().__init__(placeholder="選んでください", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"選択: {self.values[0]}")


class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MySelect({}))

async def menu(interaction: discord.Interaction):
    await interaction.response.send_message("選択してください", view=MyView())