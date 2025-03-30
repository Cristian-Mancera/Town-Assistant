import discord
from discord.ext import commands

class FormatChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="formatchannel", description="Gets the API format of a channel.")
    async def format_channel(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        await interaction.response.send_message(
            content=f"API format for {channel.mention}:\n```{channel.mention}```",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(FormatChannel(bot))
