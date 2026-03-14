from datetime import datetime, timezone

import discord
from discord import AuditLogAction

# ——— AuditLog 検索ヘルパー ———
async def fetch_audit_entry(
    guild: discord.Guild,
    action: AuditLogAction,
    target_id: int,
    *,
    lookback: float = 15.0
) -> discord.AuditLogEntry | None:
    now = datetime.now(timezone.utc)
    async for entry in guild.audit_logs(limit=10, action=action):
        target = entry.target
        if target is None:
            continue
        # target が id 属性を持たない可能性もあるため安全に取得
        if getattr(target, "id", None) == target_id:
            if (now - entry.created_at).total_seconds() <= lookback:
                return entry
    return None