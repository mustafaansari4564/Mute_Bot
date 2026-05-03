# Mute Bot - Assigns mute role to mentioned user

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
import time

# ── Keep-alive server ─────────────────────────────────────────────────────────

app = Flask('')

@app.route('/')
def home():
    return "Mute Bot is alive! 🤖"

Thread(target=run_flask := lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

load_dotenv()

TOKEN           = os.getenv("DISCORD_TOKEN")
ALLOWED_ROLE_ID = int(os.getenv("ALLOWED_ROLE_ID", "0"))  # Role ID allowed to use !mute
MUTE_ROLE_ID    = int(os.getenv("MUTE_ROLE_ID", "0"))     # Role ID to assign (mute role)

# ── Bot setup ─────────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ── Helper ────────────────────────────────────────────────────────────────────

def has_allowed_role(member: discord.Member) -> bool:
    return any(role.id == ALLOWED_ROLE_ID for role in member.roles)

# ── Events ────────────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Allowed Role ID : {ALLOWED_ROLE_ID}")
    print(f"Mute Role ID    : {MUTE_ROLE_ID}")

# ── Commands ──────────────────────────────────────────────────────────────────

@bot.command(name="mute")
async def mute(ctx, member: discord.Member = None):
    """Assign mute role to a mentioned user  |  !mute @user"""

    # 1) Check if command giver has the allowed role
    if not has_allowed_role(ctx.author):
        embed = discord.Embed(
            description="❌ You are not allowed to use this command.",
            color=0xff0000
        )
        await ctx.reply(embed=embed)
        return

    # 2) Check if a member was mentioned
    if member is None:
        embed = discord.Embed(
            description="⚠️ Please mention a user.\n**Usage:** `!mute @user`",
            color=0xffa500
        )
        await ctx.reply(embed=embed)
        return

    # 3) Prevent muting yourself
    if member == ctx.author:
        embed = discord.Embed(
            description="⚠️ You cannot mute yourself.",
            color=0xffa500
        )
        await ctx.reply(embed=embed)
        return

    # 4) Prevent muting bots
    if member.bot:
        embed = discord.Embed(
            description="⚠️ You cannot mute a bot.",
            color=0xffa500
        )
        await ctx.reply(embed=embed)
        return

    # 5) Check if already muted
    mute_role = ctx.guild.get_role(MUTE_ROLE_ID)
    if mute_role is None:
        embed = discord.Embed(
            description="❌ Mute role not found. Check `MUTE_ROLE_ID` in your `.env` file.",
            color=0xff0000
        )
        await ctx.reply(embed=embed)
        return

    if mute_role in member.roles:
        embed = discord.Embed(
            description=f"⚠️ {member.mention} is already muted.",
            color=0xffa500
        )
        await ctx.reply(embed=embed)
        return

    # 6) Assign mute role
    try:
        await member.add_roles(mute_role, reason=f"Muted by {ctx.author} ({ctx.author.id})")
        embed = discord.Embed(
            title="🔇 User Muted",
            color=0x00f3ff
        )
        embed.add_field(name="👤 Muted User", value=f"{member.mention} (`{member.id}`)", inline=False)
        embed.add_field(name="🛡️ Muted By",   value=f"{ctx.author.mention}",             inline=False)
        embed.set_footer(text=f"Role assigned: {mute_role.name}")
        await ctx.reply(embed=embed)

    except discord.Forbidden:
        embed = discord.Embed(
            description="❌ I don't have permission to assign roles. Make sure my role is above the mute role.",
            color=0xff0000
        )
        await ctx.reply(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            description=f"❌ Something went wrong: `{e}`",
            color=0xff0000
        )
        await ctx.reply(embed=embed)


@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member = None):
    """Remove mute role from a mentioned user  |  !unmute @user"""

    # 1) Check if command giver has the allowed role
    if not has_allowed_role(ctx.author):
        embed = discord.Embed(
            description="❌ You are not allowed to use this command.",
            color=0xff0000
        )
        await ctx.reply(embed=embed)
        return

    # 2) Check if a member was mentioned
    if member is None:
        embed = discord.Embed(
            description="⚠️ Please mention a user.\n**Usage:** `!unmute @user`",
            color=0xffa500
        )
        await ctx.reply(embed=embed)
        return

    # 3) Get mute role
    mute_role = ctx.guild.get_role(MUTE_ROLE_ID)
    if mute_role is None:
        embed = discord.Embed(
            description="❌ Mute role not found. Check `MUTE_ROLE_ID` in your `.env` file.",
            color=0xff0000
        )
        await ctx.reply(embed=embed)
        return

    # 4) Check if actually muted
    if mute_role not in member.roles:
        embed = discord.Embed(
            description=f"⚠️ {member.mention} is not muted.",
            color=0xffa500
        )
        await ctx.reply(embed=embed)
        return

    # 5) Remove mute role
    try:
        await member.remove_roles(mute_role, reason=f"Unmuted by {ctx.author} ({ctx.author.id})")
        embed = discord.Embed(
            title="🔊 User Unmuted",
            color=0x00ff00
        )
        embed.add_field(name="👤 Unmuted User", value=f"{member.mention} (`{member.id}`)", inline=False)
        embed.add_field(name="🛡️ Unmuted By",   value=f"{ctx.author.mention}",             inline=False)
        embed.set_footer(text=f"Role removed: {mute_role.name}")
        await ctx.reply(embed=embed)

    except discord.Forbidden:
        embed = discord.Embed(
            description="❌ I don't have permission to remove roles.",
            color=0xff0000
        )
        await ctx.reply(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            description=f"❌ Something went wrong: `{e}`",
            color=0xff0000
        )
        await ctx.reply(embed=embed)


@bot.command(name="guide")
async def guide(ctx):
    embed = discord.Embed(
        title="📖 Mute Bot — Guide",
        color=0x00f3ff
    )
    embed.add_field(name="🔇 Mute a user",   value="`!mute @user`",   inline=False)
    embed.add_field(name="🔊 Unmute a user", value="`!unmute @user`", inline=False)
    embed.add_field(name="📖 Guide",         value="`!guide`",        inline=False)
    embed.set_footer(text="Only allowed roles can use mute/unmute commands.")
    await ctx.reply(embed=embed)


@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")


if __name__ == "__main__":
    print("⏳ Starting bot...")
    time.sleep(3)
    bot.run(TOKEN, reconnect=True, log_handler=None)
