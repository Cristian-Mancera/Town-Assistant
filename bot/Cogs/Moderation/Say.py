import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="say", description="Sends a message through the bot.")
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def say(self, interaction: discord.Interaction, message: str):
        if not message.strip():
            await interaction.response.send_message("You must provide a message to send.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)  # Prevent errors while sending the message

        try:
            await interaction.channel.send(content=message)
            await interaction.followup.send("Message sent.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to send messages in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Say(bot))
