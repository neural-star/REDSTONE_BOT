import discord

def has_wiki_role(interaction: discord.Interaction, role_id:int) -> bool:
    if interaction.guild is None:
        return False
    member = interaction.user
    if not isinstance(member, discord.Member):
        member = interaction.guild.get_member(interaction.user.id)
        if member is None:
            return False
    return any(role.id == role_id for role in member.roles)