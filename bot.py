import discord
from discord.ext import commands
from discord import app_commands, ui
from typing import Literal
from config import TOKEN

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

#Stage 2 of the modal
class HFI_modal(ui.Modal, title="Incident Report"):
    in_game_day = ui.TextInput(label="In-game day", placeholder="e.g. \"Day:\" ##", min_length=1)
    location = ui.TextInput(label="Location",placeholder="Where the incident occured")
    car_id = ui.TextInput(label="Car ID(s)",placeholder="e.g. IOS475, FLP909,...")
    condition = ui.TextInput(label="Current condition(s) in order of car ID(s)")
    description = ui.TextInput(label="Brief description of what happened", style=discord.TextStyle.paragraph)

    def __init__(self,road:str):
        super().__init__()
        self.road = road

    async def on_submit(self, interaction: discord.Interaction):
        summary = (
            f"🚂**Road**: {self.road}\n"
            f"📅 **Day**: {self.in_game_day.value}\n"
            f"📍 **Location**: {self.location.value}\n"
            f"🚃 **Car ID(s)**: {self.car_id.value}\n"
            f"🤕 **Current condition(s)**: {self.condition.value}\n"
            f"📝 **Description of what happened**: {self.description.value}"
        )
        await interaction.response.send_message(summary)


# Stage 1: Slash command to report a car incident
@bot.tree.command(name="hfi", description="Make a report")
@app_commands.describe(road="Choose a Railroad")
async def hfi(
    interaction: discord.Interaction,
    road: Literal["TVRC","CBR"]
):
    await interaction.response.send_modal(HFI_modal(road=road))


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

bot.run(TOKEN)