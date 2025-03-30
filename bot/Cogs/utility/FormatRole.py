import discord
from discord.ext import commands

class FormatRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="formatrole", description="Gets the format of a role.")
    async def format_role(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.send_message(
            content=f"API format for {role.mention}:\n```{role.mention}```",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(FormatRole(bot))
