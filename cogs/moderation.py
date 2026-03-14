from datetime import datetime
from typing import cast

import discord
from discord import AuditLogAction

from config import client, LOG_CHANNEL_ID
from utils import fetch_audit_entry

if LOG_CHANNEL_ID:
    LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)

@client.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    log_ch = cast(discord.TextChannel, guild.get_channel(LOG_CHANNEL_ID))
    if not log_ch:
        return

    kick_entry = await fetch_audit_entry(guild, AuditLogAction.kick, member.id)
    if kick_entry:
        reason = kick_entry.reason or "なし"
        ts = kick_entry.created_at.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        await log_ch.send(
            f"🚪 **{member}** がキックされました\n"
            f"→ 実行者: **{kick_entry.user}**\n"
            f"→ 時間: `{ts}`\n"
            f"→ 理由: {reason}"
        )
        return

    await log_ch.send(f"👋 **{member}** が退出しました")

@client.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    log_ch = cast(discord.TextChannel, guild.get_channel(LOG_CHANNEL_ID))
    if not log_ch:
        return

    ban_entry = await fetch_audit_entry(guild, AuditLogAction.ban, user.id)
    if ban_entry:
        reason = ban_entry.reason or "なし"
        ts = ban_entry.created_at.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        await log_ch.send(
            f"🔨 **{user}** が BAN されました\n"
            f"→ 実行者: **{ban_entry.user}**\n"
            f"→ 時間: `{ts}`\n"
            f"→ 理由: {reason}"
        )
    else:
        now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
        await log_ch.send(f"🔨 **{user}** が BAN されました\n→ 時間: `{now}`")