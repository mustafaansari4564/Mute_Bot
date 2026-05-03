# 🔇 Mute Bot — Discord Role Manager

A simple but powerful Discord bot that allows **authorized staff members** to mute and unmute users by assigning/removing a mute role — all with a single command.

---

## ⚡ Commands

| Command | Description |
|---------|-------------|
| `$mute @user` | Assigns the mute role to a user |
| `$unmute @user` | Removes the mute role from a user |
| `$guide` | Shows all available commands |
| `$ping` | Check bot latency |

---

## 🔐 How Authorization Works

```
User types: $mute @someone
        ↓
Bot checks: Does the command giver have ALLOWED_ROLE_ID?
        ↓
   YES → Assigns MUTE_ROLE_ID to @someone ✅
   NO  → ❌ "You are not allowed to use this command."
```

Only members with the **allowed role** can use `$mute` and `$unmute`. Everyone else gets denied automatically.

---

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `DISCORD_TOKEN` | Your Discord bot token |
| `ALLOWED_ROLE_ID` | Role ID of members allowed to use `$mute` / `$unmute` |
| `MUTE_ROLE_ID` | Role ID that gets assigned to muted users |

### 3. Run the Bot
```bash
python bot.py
```

---

## 📋 .env Example

```env
DISCORD_TOKEN=your_discord_bot_token_here
ALLOWED_ROLE_ID=123456789012345678
MUTE_ROLE_ID=987654321098765432
```

---

## 🗂️ File Structure

```
📁 Mute_bot/
   ├── bot.py              ← Main bot file
   ├── requirements.txt    ← Python dependencies
   ├── .env                ← Your secret keys (never share this!)
   └── README.md           ← This file
```

---

## ⚠️ Important Discord Settings

Before running the bot, make sure:

1. Go to **Discord Developer Portal** → Your Bot → **Bot** tab
2. Enable **Server Members Intent** ✅
3. Enable **Message Content Intent** ✅
4. Make sure the bot's role is **above the mute role** in your server's role hierarchy

---

## 🔒 Safety Features

- ✅ Cannot mute yourself
- ✅ Cannot mute other bots
- ✅ Tells you if user is already muted
- ✅ Tells you if user is not muted (on unmute)
- ✅ Only authorized roles can run commands
- ✅ Clear error messages if something goes wrong

---

## 🚀 Hosting on Kerit / HeavenCloud

Use this as your startup command:
```bash
python bot.py
```

Or if running multiple bots together, include it in your `start.py` launcher.

---

## 📦 Requirements

```
discord.py
python-dotenv
flask
```
