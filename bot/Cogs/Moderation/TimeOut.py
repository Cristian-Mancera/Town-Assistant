import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class TimeOut(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="timeout",
        description="Puts a user in timeout for a specific duration."
    )
    @app_commands.describe(
        user="The user you want to timeout.",
        duration="Select a duration for the timeout.",
        reason="Optional reason for the timeout."
    )
    @app_commands.choices(
        duration=[
            app_commands.Choice(name="60 seconds", value=60),
            app_commands.Choice(name="5 minutes", value=5 * 60),
            app_commands.Choice(name="10 minutes", value=10 * 60),
            app_commands.Choice(name="1 hour", value=60 * 60),
            app_commands.Choice(name="12 hours", value=12 * 60 * 60),
            app_commands.Choice(name="1 day", value=24 * 60 * 60),
            app_commands.Choice(name="15 days", value=15 * 24 * 60 * 60),
            app_commands.Choice(name="1 week", value=7 * 24 * 60 * 60),
        ]
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: app_commands.Choice[int],
        reason: str = ""
    ):
        timeout_duration = timedelta(seconds=duration.value)

        try:
            await user.timeout(timeout_duration, reason=reason)

            embed = discord.Embed(
                title="User Timed Out",
                description=(
                    f"**User:** {user.mention}\n"
                    f"**ID:** {user.id}\n\n"
                    f"**Reason:** {reason}"
                ),
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to timeout this user.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"An error occurred while trying to timeout the user: {e}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(TimeOut(bot))
