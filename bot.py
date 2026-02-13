import os, discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash command to report a car incident
@bot.tree.command(name="hfi", description="Make a report")
@app_commands.describe(
    In_game_day="In-game day of the incident (e.g. \"Day:\" ##)",
    Location="Where the incident occured",
    Car_id="Car identification number(s) (e.g. IOS475, FLP909,...)",
    Condition="Current condition(s) in order of car ID(s)",
    Description="Brief description of what happened"
)
async def hfi(
    interaction: discord.Interaction,
    In_game_day: str,
    Location: str,
    Car_id: str,
    Condition: str,
    Description: str
):
    # Compose and send the response
    summary = (
        f"📅 **Day**: {In_game_day}\n"
        f"📍 **Location**: {Location}\n"
        f"🚃 **Car ID(s)**: {Car_id}\n"
        f"🤕 **Current condition(s)**: {Condition}\n"
        f"📝 **Description of what happened**: {Description}"
    )
    await interaction.response.send_message(summary)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

keep_alive()
bot.run(os.environ["TOKEN"])