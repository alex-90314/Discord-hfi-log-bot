import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash command to report a car incident
@bot.tree.command(name="hfi", description="Make a report")
@app_commands.describe(
    road="Choose an alternate RR"
    in_game_day="In-game day of the incident (e.g. \"Day:\" ##)",
    location="Where the incident occured",
    car_id="Car identification number(s) (e.g. IOS475, FLP909,...)",
    condition="Current condition(s) in order of car ID(s)",
    description="Brief description of what happened"
)
async def hfi(
    interaction: discord.Interaction,
    road: Literal["Road2", "Road3"] = "TVRC",
    in_game_day: str,
    location: str,
    car_id: str,
    condition: str,
    description: str
):
    # Compose and send the response
    summary = (
        f"🚂**Road**{road}\n"
        f"📅 **Day**: {in_game_day}\n"
        f"📍 **Location**: {location}\n"
        f"🚃 **Car ID(s)**: {car_id}\n"
        f"🤕 **Current condition(s)**: {condition}\n"
        f"📝 **Description of what happened**: {description}"
    )
    await interaction.response.send_message(summary)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

bot.run(os.environ["TOKEN"])