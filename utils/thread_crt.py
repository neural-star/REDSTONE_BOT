from typing import Optional, List, cast

import discord

from config import client

async def create_thread(
    *,
    interaction: Optional[discord.Interaction] = None,
    channel_id: int,
    name: str,
    reason: str = "",
    server_id: Optional[int] = None,
    lock: bool = False,
    restrict_role_ids: Optional[List[int]] = None
) -> Optional[discord.Thread]:
    guild: Optional[discord.Guild] = None
    if server_id:
        guild = client.get_guild(server_id)
    elif interaction and interaction.guild:
        guild = interaction.guild

    if guild is None:
        return None

    channel = cast(Optional[discord.TextChannel], guild.get_channel(channel_id))
    if channel is None:
        return None

    for th in channel.threads:
        if th.name == name:
            return th

    thread = await channel.create_thread(
        name=name,
        reason=reason,
        type=discord.ChannelType.public_thread
    )

    if lock:
        await thread.edit(locked=True)

    return thread