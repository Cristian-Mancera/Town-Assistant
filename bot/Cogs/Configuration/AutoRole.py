import discord
from discord.ext import commands
from discord import app_commands
import json
import datetime
import os

AUTOROLE_FILE = "Data/AutoRoles.json"

def load_autoroles():
    if not os.path.exists(AUTOROLE_FILE):
        return {}
    with open(AUTOROLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_autoroles(data):
    with open(AUTOROLE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class AutoRolesAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="autorole_add", description="Assign an automatic role to new server members.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def autorole_add(self, interaction: discord.Interaction, role: discord.Role):
        autoroles = load_autoroles()
        guild_id = str(interaction.guild.id)
        old_role = None

        if guild_id in autoroles:
            old_role = autoroles[guild_id]["role_id"]
        
        autoroles[guild_id] = {"role_name": role.name, "role_id": role.id}
        save_autoroles(autoroles)

        embed = discord.Embed(
            title="SUCCESSFUL ASSIGNMENT",
            color=0x00FF00 
        )
        embed.description = f"The role {role.mention} has been successfully assigned to new server members."
        if old_role and old_role != role.id:
            old_role_obj = interaction.guild.get_role(old_role)
            if old_role_obj:
                embed.description += f"\nAnd the role {old_role_obj.mention} has been removed as an automatic role."
        
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.datetime.now()  

        await interaction.response.send_message(embed=embed)

class AutoRolesRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="autorole_remove", description="Remove the assigned automatic role for new users.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def autorole_remove(self, interaction: discord.Interaction):
        autoroles = load_autoroles()
        guild_id = str(interaction.guild.id)

        if guild_id in autoroles:
            role_id = autoroles[guild_id]["role_id"]
            role = interaction.guild.get_role(role_id)
            del autoroles[guild_id]
            save_autoroles(autoroles)

            embed = discord.Embed(
                title="SUCCESSFUL ACTION",
                description=f"The role {role.mention} has been successfully removed as an automatic assignment role.",
                color=0x57F287  
            )
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.timestamp = datetime.datetime.now()  

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("There is no automatic role assigned on this server.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(AutoRolesAdd(bot))
    await bot.add_cog(AutoRolesRemove(bot))