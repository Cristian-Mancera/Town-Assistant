import discord
import json
import os
from discord.ext import commands

COUNTER_FILE = "../Data/Counter.json"

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter_data = self.load_counter_data()

    def load_counter_data(self):
        if not os.path.exists('Data'):
            os.makedirs('Data')

        if not os.path.isfile(COUNTER_FILE):
            with open(COUNTER_FILE, "w") as f:
                json.dump({}, f, indent=4)

        with open(COUNTER_FILE, "r") as f:
            return json.load(f)

    def save_counter_data(self):
        try:
            if not os.path.exists('Data'):
                os.makedirs('Data')

            with open(COUNTER_FILE, "w") as f:
                json.dump(self.counter_data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    @discord.app_commands.command(name="counterchannel", description="Set up the counting channel")
    @discord.app_commands.checks.has_permissions(manage_channels=True)
    async def counterchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        
        guild_id = str(interaction.guild.id) 
        self.counter_data[guild_id] = {
            "channel_id": channel.id, 
            "current_number": 1 
        }
        self.save_counter_data()
        await interaction.response.send_message(f"Counting channel successfully assigned to: {channel.mention}.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        guild_id = str(message.guild.id) 
        if guild_id in self.counter_data:
            channel_id = self.counter_data[guild_id]["channel_id"]  
            current_number = self.counter_data[guild_id]["current_number"] 

            if message.channel.id == channel_id:
                try:
                    num = int(message.content)
                    if num == current_number:
                        # The number is correct
                        await message.add_reaction("<a:right:1334620322128724039>")
                        self.counter_data[guild_id]["current_number"] += 1
                        self.save_counter_data()
                    else:
                        await message.add_reaction("<a:wrong_cross:1334620377577422889>") 
                        await message.channel.send(f"YOU MADE A MISTAKE AT {current_number}, {message.author.mention}!\n→ The counter resets to 1.")
                        # Reset the counter
                        self.counter_data[guild_id]["current_number"] = 1
                        self.save_counter_data()

                except ValueError:
                    await message.add_reaction("<a:wrong_cross:1334620377577422889>") 
                    await message.channel.send(
                        f"{message.author.mention} This is a counting channel. " 
                        "It is not a chat channel. For this reason, the counter resets to 1."
                    )
                    # Reset the counter
                    self.counter_data[guild_id]["current_number"] = 1
                    self.save_counter_data()

async def setup(bot):
    await bot.add_cog(Counter(bot))