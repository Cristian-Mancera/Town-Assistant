import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="unban", description="Revokes a user's ban.")
    @discord.app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str, *, reason: str = None):
        if reason is None:
            reason = ""

        try:
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                "Please provide a valid user ID.", ephemeral=True
            )
            return

        if not interaction.guild.me.guild_permissions.ban_members:
            await interaction.response.send_message(
                "I don't have permission to unban members.", ephemeral=True
            )
            return

        try:
            user = await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user, reason=reason)
            
            embed = discord.Embed(
                title="Unban Successful",
                description=(
                    f"**User:** {user.mention}\n"
                    f"**ID:** {user.id}\n\n"
                    f"**Reason:** {reason}"
                ),
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            embed.set_footer(text=f"Unbanned by {interaction.user}", icon_url=interaction.user.avatar.url)

            await interaction.response.send_message(embed=embed)
        except discord.NotFound:
            await interaction.response.send_message(
                "No user found with that ID.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                f"I don't have permission to unban {user.mention}.", ephemeral=True
            )
        except discord.HTTPException:
            await interaction.response.send_message(
                "An error occurred while trying to unban the user.", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"An unexpected error occurred: {str(e)}", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Unban(bot))
