import discord, json
from discord.ext import commands, tasks
from discord import app_commands
from keep_alive import keep_alive
from datetime import datetime, timedelta
from collections import Counter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

LOG_FILE = "reports.json"

def load_reports():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_reports(reports):
    with open(LOG_FILE, "w") as f:
        json.dump(reports, f, default=str)

SECRET_PATH = "/etc/secrets/reports.json"

try:
    with open(SECRET_PATH, "r", encoding="utf-8") as f:
        reports = json.load(f)
        print("Loaded reports from secret file:", reports)
except FileNotFoundError:
    print("No reports secret file found.")
    reports = []


# last_response_date = {} # Dictionary to track the last response date per guild
# @bot.event
# async def on_message(message):
#     # Prevent the bot from responding to its own messages
#     if message.author == bot.user:
#         return

#     # Check if the message is in the 'general' channel
#     if message.channel.name == "general":
#         role = discord.utils.get(message.guild.roles, name="Railroader Game") # Retrieve the role by name
#         if role and role in message.role_mentions:
#             keywords = "Server is up"
#             if (keyword in message.content.lower() for keyword in keywords):
#                 current_day = datetime.utcnow().day # Get the current day of the month
#                 if current_day%3==0: # Check if the day is divisible by 3
#                     guild_id = message.guild.id
#                     if last_response_date.get(guild_id) != current_day: # Check if the bot has already responded today
#                         await message.channel.send("Fellow reminder to keep yours eyes and ears open less you want to have a meeting in my office. 👀😁")
#                         last_response_date[guild_id] = current_day # Update the last response date
    
#     await bot.process_commands(message) # Process other commands if any


@bot.tree.command(name="test_report", description="Run the report now (test only)")
async def test_report(interaction: discord.Interaction):
    # This reuses your existing logic
    now = datetime.utcnow()
    two_weeks_ago = now - timedelta(days=14)
    reports = load_reports()
    recent = [r for r in reports if datetime.fromisoformat(r["timestamp"]) >= two_weeks_ago]

    total = len(recent)
    avg_per_day = total / 14 if total else 0
    days = [datetime.fromisoformat(r["timestamp"]).date() for r in recent]
    most_common = Counter(days).most_common(1)
    top_day = most_common[0][0].isoformat() if most_common else "N/A"

    await interaction.response.send_message(
        f"**Bi-Weekly Test Report**\n"
        f"• Total incidents: {total}\n"
        f"• Average per day: {avg_per_day:.2f}\n"
        f"• Busiest day: {top_day}", ephemeral=True
    )


# Slash command to report a car incident
@bot.tree.command(name="hfi", description="Make a report")
@app_commands.describe(
    date="Date of the incident (e.g. Day ##)",
    location="Where the incident occured",
    car_id="Car identification number(s) (e.g. IOS475, FLP909,...)",
    percent="Current condition(s) in order of car ID(s)",
    description="Brief description of what happened"
)
async def hfi(
    interaction: discord.Interaction,
    date: str,
    location: str,
    car_id: str,
    percent: str,
    description: str
):
    # Compose and send the response
    report = (
        f"📅 **Day**: {date}\n"
        f"📍 **Location**: {location}\n"
        f"🚃 **Car ID(s)**: {car_id}\n"
        f"🤕 **Current condition(s)**: {percent}\n"
        f"📝 **Description of what happened**: {description}"
    )
    reports = load_reports()
    reports.append(report)
    save_reports(reports)
    await interaction.response.send_message(report)


@tasks.loop(hours=24)
async def biweekly_summary():
    now = datetime.utcnow()
    two_weeks_ago = now.isoformat()
    cutoff = now - timedelta(days=14)
    reports = load_reports()
    recent = [r for r in reports if datetime.fromisoformat(r["timestamp"]) >= now - timedelta(days=14)]
    total = len(recent)
    avg_per_day = (total / 14) if total else 0
    days = [datetime.fromisoformat(r["timestamp"]).date() for r in recent]
    most_common = Counter(days).most_common(1)
    top_day = most_common[0][0].isoformat() if most_common else "N/A"

    channel = bot.get_channel("SUMMARY_CHANNEL")
    asyncio.create_task(channel.send(
        f"**Bi-Weekly Incident Report**\n"
        f"• Total incidents: {total}\n"
        f"• Average per day: {avg_per_day:.2f}\n"
        f"• Most incidents on: {top_day}"
    ))

    # Clear logs after reporting
    save_reports([])


@biweekly_summary.before_loop
async def before_summary():
    await bot.wait_until_ready()


class MyBot(discord.Bot):
    async def setup_hook(self):
        # Initialize the scheduler within the asynchronous setup_hook
        self.scheduler = AsyncIOScheduler()
        trigger = CronTrigger(day='1st mon,3rd mon', hour=10, minute=0)
        self.scheduler.add_job(biweekly_summary, trigger)
        self.scheduler.start()
        
    async def on_ready(self):
        print(f'Logged in as {self.user}')


keep_alive()
bot = MyBot()
bot.run("token")