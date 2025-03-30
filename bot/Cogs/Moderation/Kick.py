import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="kick", description="Kicks a user from the server.")
    @discord.app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        if reason is None:
            reason = ""

        if not interaction.guild.me.guild_permissions.kick_members:
            await interaction.response.send_message(
                "I do not have permission to kick members.", ephemeral=True
            )
            return

        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I cannot kick this member as they have a role equal to or higher than mine.", ephemeral=True
            )
            return

        try:
            await member.kick(reason=reason)
            
            # Create the embed
            embed = discord.Embed(
                title="Kick Successful",
                description=(
                    f"**User:** {member.mention}\n"
                    f"**ID:** {member.id}\n\n"
                    f"**Reason:** {reason}"
                ),
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            embed.set_footer(text=f"Kicked by {interaction.user}", icon_url=interaction.user.avatar.url)

            # Send the embed
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                f"I do not have permission to kick {member.mention}.", ephemeral=True
            )
        except discord.HTTPException:
            await interaction.response.send_message(
                "An error occurred while trying to kick the user.", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Kick(bot))
