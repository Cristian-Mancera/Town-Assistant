import discord
from discord.ext import commands

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="addrole", description="Assigns a role to a user.")
    @discord.app_commands.checks.has_permissions(manage_roles=True)
    async def addrole(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await interaction.response.send_message(f"{user.mention} already has this role assigned.", ephemeral=True)
            return
        
        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I cannot assign this role because it is higher than my hierarchy.", ephemeral=True
            )
            return
        
        if role.name == "@everyone":
            await interaction.response.send_message("The @everyone role cannot be assigned.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message(
                "I do not have permission to manage roles.", ephemeral=True
            )
            return

        try:
            await user.add_roles(role)
            await interaction.response.send_message(
                f"The role {role.mention} has been successfully assigned to {user.mention}.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to assign this role.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred while assigning the role: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AddRole(bot))
