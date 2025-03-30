import discord
from discord.ext import commands


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="purge", description="Deletes a specific number of messages in a channel.")
    @discord.app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):

        if amount < 2 or amount > 100:
            await interaction.response.send_message(
                "Please specify a number between 2 and 100.", ephemeral=True
            )
            return

        if not interaction.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "I do not have permission to manage messages.", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"{len(deleted)} messages have been deleted.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I do not have permission to delete messages in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(f"An error occurred while deleting messages: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Purge(bot))
