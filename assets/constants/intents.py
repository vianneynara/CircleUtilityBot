import disnake
# Intents for the bot, please disable unused intents.

INTENTS = disnake.Intents(
    bans=True,
    dm_messages=True,
    dm_reactions=False,
    dm_typing=False,
    emojis=True,
    guild_messages=True,
    guild_reactions=False,
    guild_scheduled_events=False,
    guild_typing=False,
    guilds=True,
    integrations=False,
    invites=False,
    members=True,
    message_content=True,
    messages=True,
    presences=True,
    reactions=False,
    typing=False,
    voice_states=False,
    webhooks=False,
)