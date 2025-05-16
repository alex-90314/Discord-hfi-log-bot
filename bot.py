import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_count = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == bot.user:
        return

    # Check if the message is in the #general channel
    if message.channel.name == "general":
        # Check if 'Railroader Game' is mentioned in the message
        if any(user.name == "Railroader Game" for user in message.mentions):
            await message.channel.send("Fellow reminder to keep yours eyes and ears open less you want to have a meeting in my office.😊")

    # Process other commands if any
    await bot.process_commands(message)

# Slash command to report a car incident
@bot.tree.command(name="hfi", description="Make a report")
@app_commands.describe(
    date="Date of the incident (e.g. Day ##)",
    location="Where the incident occured",
    car_id="Car identification number(s) (e.g. IOS475, FLP909,...)",
    percent="Current percentage(s) in order of car ID(s)",
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
    summary = (
        f"📅 **Day**: {date}\n"
        f"📍 **Location**: {location}\n"
        f"🚃 **Car ID(s)**: {car_id}\n"
        f"🤕 **Current damage(s)**: {percent}\n"
        f"📝 **Description of what happened**: {description}"
    )
    await interaction.response.send_message(summary)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

keep_alive()
bot.run(os.environ["token"])
