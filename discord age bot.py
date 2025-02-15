import discord
import os 
import asyncio
from discord.ext import commands


TOKEN = "YOUR_BOT_TOKEN"
MOD_CHANNEL_ID = 123456789012345678  # Replace with your moderator channel ID
GUILD_ID = 123456789012345678  # Replace with your server ID
AGE_ROLE_IDS = [1334658209624883340, 1334658365196079176, 1334658551213326410,1334658711486070919,1334659023534035055,1334659193843617935,1334659384323870790,1334659557867126814]
WAIT_TIME =  16*3600

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_member_join(member):
    if member.bot:
        return
    
    try:
        await member.send("👋 Welcome! Please get your age role within an appropriate time frame. "
    "This is a warning—if you do not select an age role within **16 hours**, you will be banned.")
    except Exception as e:
        print(f"Failed to send message to {member.name}: {e}")

    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(member.id)

    if not any(role.id in AGE_ROLE_IDS for role in member.roles):
        await asyncio.sleep(WAIT_TIME)
        if not any(role.id in AGE_ROLE_IDS for role in member.roles):
            await member.ban(reason="Failed to get age role within 16 hours")

            
async def check_members_for_age_role():
    banned_count = 0
    guild = bot.get_guild(GUILD_ID)
    for member in guild.members:
        if not member.bot and not any(role.id in AGE_ROLE_IDS for role in member.roles):
            try:
                await member.send("⛔ You didn’t select an age role in time. You have been removed.")
            except Exception as e:
                print(f"Failed to send message to {member.name}: {e}")
            await member.kick(reason="Did not select an age role in time.")
            banned_count += 1

    await guild.system_channel.send(f"✅ **{banned_count} users** were kicked for not selecting an age role.")

@bot.event
async def on_ready():
    await check_members_for_age_role()

async def ban_unaged_members():
    guild = bot.get_guild(GUILD_ID)
    for member in guild.members:
        if member.banned:
            log_channel = bot.get_channel(MOD_CHANNEL_ID)
            await log_channel.send(f"{member.name} has been banned for not selecting an age role in time.")
            await member.ban(reason="Did not select an age role in time.")
            await asyncio.sleep(1)

@bot.event
async def on_ready():
    await check_members_for_age_role()
    await ban_unaged_members()


bot.run(TOKEN)



    


