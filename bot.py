import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFICATION_CHANNEL_ID = 1359921415549096187
WELCOME_CHANNEL_ID = 1359908452176105503
NEED_VERIFICATION_ROLE = "NEED VERIFICATION"
STUDENT_ROLE = "STUDENT"
ADMIN_ROLE = "Admin"

@bot.event
async def on_ready():
    print(f'Bot je aktivan kao {bot.user}!')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != VERIFICATION_CHANNEL_ID:
        return

    if str(payload.emoji.name) != "✅":
        return

    guild = bot.get_guild(payload.guild_id)
    member_reacting = guild.get_member(payload.user_id)

    admin_role = discord.utils.get(guild.roles, name=ADMIN_ROLE)
    if admin_role not in member_reacting.roles:
        return

    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user_to_verify = message.author

    need_verification_role = discord.utils.get(guild.roles, name=NEED_VERIFICATION_ROLE)
    student_role = discord.utils.get(guild.roles, name=STUDENT_ROLE)

    await user_to_verify.remove_roles(need_verification_role)
    await user_to_verify.add_roles(student_role)

    welcome_channel = guild.get_channel(WELCOME_CHANNEL_ID)
    await welcome_channel.send(f"Welcome {user_to_verify.mention}! You have been successfully verified and now have full access to the server!")

    await user_to_verify.send(
        "Hello! You have been successfully verified and now have full access to the server. Welcome!"
    )

bot.run(os.getenv('TOKEN'))
